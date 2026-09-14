"""SQLite persistence, migrations, audit and agent identity."""
from __future__ import annotations
import json, sqlite3, hashlib
from datetime import datetime
from pathlib import Path
from typing import Any
from .schema import Habitat, Job, Signal, Action
from .claims import Claim

SCHEMA_VERSION=2
SCHEMA="""
CREATE TABLE IF NOT EXISTS schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS habitat (id TEXT PRIMARY KEY, name TEXT NOT NULL, model TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS job (id TEXT PRIMARY KEY, habitat_id TEXT NOT NULL, name TEXT NOT NULL, schedule TEXT, enabled INTEGER NOT NULL, command TEXT, last_run_at TEXT, last_status TEXT, failure_streak INTEGER NOT NULL, last_error TEXT);
CREATE TABLE IF NOT EXISTS signal (id TEXT PRIMARY KEY, habitat_id TEXT NOT NULL, job_id TEXT, type TEXT NOT NULL, severity TEXT NOT NULL, code TEXT NOT NULL, message TEXT NOT NULL, detected_at TEXT NOT NULL, resolved_at TEXT, data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS action (id TEXT PRIMARY KEY, habitat_id TEXT NOT NULL, job_id TEXT, timestamp TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, status TEXT NOT NULL, details TEXT NOT NULL, run_id TEXT);
CREATE TABLE IF NOT EXISTS claim (id TEXT PRIMARY KEY, habitat_id TEXT NOT NULL, job_id TEXT, claim TEXT NOT NULL, action TEXT, expected_status TEXT NOT NULL, created_at TEXT NOT NULL, verified_at TEXT, status TEXT NOT NULL, evidence TEXT NOT NULL, run_id TEXT);
CREATE TABLE IF NOT EXISTS event (id TEXT PRIMARY KEY, habitat_id TEXT NOT NULL, type TEXT NOT NULL, received_at TEXT NOT NULL, signature_valid INTEGER NOT NULL, payload TEXT NOT NULL, correlation_id TEXT, agent_id TEXT);
CREATE TABLE IF NOT EXISTS agent (id TEXT PRIMARY KEY, habitat_id TEXT NOT NULL, name TEXT NOT NULL, enabled INTEGER NOT NULL, permissions TEXT NOT NULL, secret_hash TEXT, created_at TEXT NOT NULL, last_seen_at TEXT);
CREATE INDEX IF NOT EXISTS idx_action_run ON action(run_id);
CREATE INDEX IF NOT EXISTS idx_claim_run ON claim(run_id);
CREATE INDEX IF NOT EXISTS idx_event_received ON event(received_at);
"""

def _dt(value): return datetime.fromisoformat(value) if value else None
class Store:
    def __init__(self,path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        self.conn=sqlite3.connect(self.path,timeout=10); self.conn.row_factory=sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys=ON"); self.conn.execute("PRAGMA journal_mode=WAL"); self.conn.executescript(SCHEMA); self._migrate(); self.conn.commit()
    def _migrate(self):
        cols={r[1] for r in self.conn.execute("PRAGMA table_info(event)")}
        if "agent_id" not in cols: self.conn.execute("ALTER TABLE event ADD COLUMN agent_id TEXT")
        self.conn.execute("INSERT OR IGNORE INTO schema_meta(key,value) VALUES('version','1')")
        self.conn.execute("UPDATE schema_meta SET value=? WHERE key='version'",(str(SCHEMA_VERSION),))
    def close(self): self.conn.close()
    def save_habitat(self,h): self.conn.execute("INSERT OR REPLACE INTO habitat VALUES (?,?,?,?,?,?)",(h.id,h.name,h.model,h.created_at.isoformat(),h.updated_at.isoformat(),h.status)); self.conn.commit()
    def save_job(self,j): self.conn.execute("INSERT OR REPLACE INTO job VALUES (?,?,?,?,?,?,?,?,?,?)",(j.id,j.habitat_id,j.name,j.schedule,int(j.enabled),j.command,j.last_run_at.isoformat() if j.last_run_at else None,j.last_status,j.failure_streak,j.last_error)); self.conn.commit()
    def save_signal(self,s): self.conn.execute("INSERT OR REPLACE INTO signal VALUES (?,?,?,?,?,?,?,?,?,?)",(s.id,s.habitat_id,s.job_id,s.type,s.severity,s.code,s.message,s.detected_at.isoformat(),s.resolved_at.isoformat() if s.resolved_at else None,json.dumps(s.data))); self.conn.commit()
    def save_action(self,a): self.conn.execute("INSERT OR REPLACE INTO action VALUES (?,?,?,?,?,?,?,?,?)",(a.id,a.habitat_id,a.job_id,a.timestamp.isoformat(),a.actor,a.action,a.status,json.dumps(a.details),a.run_id)); self.conn.commit()
    def habitat(self):
        r=self.conn.execute("SELECT * FROM habitat LIMIT 1").fetchone()
        if not r: raise RuntimeError("No Habitat initialized")
        return Habitat(r["id"],r["name"],r["model"],_dt(r["created_at"]),_dt(r["updated_at"]),r["status"])
    def jobs(self):
        return [Job(r["id"],r["habitat_id"],r["name"],r["schedule"],bool(r["enabled"]),r["command"],_dt(r["last_run_at"]),r["last_status"],r["failure_streak"],r["last_error"]) for r in self.conn.execute("SELECT * FROM job ORDER BY name")]
    def signals(self):
        return [Signal(r["id"],r["habitat_id"],r["type"],r["severity"],r["code"],r["message"],r["job_id"],_dt(r["detected_at"]),_dt(r["resolved_at"]),json.loads(r["data"])) for r in self.conn.execute("SELECT * FROM signal ORDER BY detected_at DESC")]
    def actions(self,limit=50):
        return [Action(r["id"],r["habitat_id"],_dt(r["timestamp"]),r["actor"],r["action"],r["status"],r["job_id"],json.loads(r["details"]),r["run_id"]) for r in self.conn.execute("SELECT * FROM action ORDER BY timestamp DESC LIMIT ?",(limit,))]
    def save_claim(self,c): self.conn.execute("INSERT OR REPLACE INTO claim VALUES (?,?,?,?,?,?,?,?,?,?,?)",(c.id,c.habitat_id,c.job_id,c.claim,c.action,c.expected_status,c.created_at.isoformat(),c.verified_at.isoformat() if c.verified_at else None,c.status,json.dumps(c.evidence),c.run_id)); self.conn.commit()
    def claims(self,limit=100):
        return [Claim(r["id"],r["habitat_id"],r["job_id"],r["claim"],r["action"],r["expected_status"],_dt(r["created_at"]),_dt(r["verified_at"]),r["status"],json.loads(r["evidence"]),r["run_id"]) for r in self.conn.execute("SELECT * FROM claim ORDER BY created_at DESC LIMIT ?",(limit,))]
    def save_event(self,event_id,habitat_id,event_type,received_at,signature_valid,payload,agent_id=None):
        cur=self.conn.execute("INSERT OR IGNORE INTO event VALUES (?,?,?,?,?,?,?,?)",(event_id,habitat_id,event_type,received_at,int(signature_valid),json.dumps(payload,sort_keys=True),payload.get("correlation_id") or payload.get("run_id"),agent_id)); self.conn.commit(); return cur.rowcount==1
    def events(self,limit=100):
        return [{"id":r["id"],"habitat_id":r["habitat_id"],"type":r["type"],"received_at":r["received_at"],"signature_valid":bool(r["signature_valid"]),"payload":json.loads(r["payload"]),"correlation_id":r["correlation_id"],"agent_id":r["agent_id"]} for r in self.conn.execute("SELECT * FROM event ORDER BY received_at DESC LIMIT ?",(limit,))]
    def active_signals(self,limit=100): return [x for x in self.signals() if x.resolved_at is None][:limit]
    @staticmethod
    def hash_secret(secret): return hashlib.sha256(secret.encode()).hexdigest()
    def save_agent(self,agent_id,habitat_id,name,enabled=True,permissions=None,secret=None):
        self.conn.execute("INSERT OR REPLACE INTO agent VALUES (?,?,?,?,?,?,?,?)",(agent_id,habitat_id,name,int(enabled),json.dumps(sorted(permissions or [])),self.hash_secret(secret) if secret else None,datetime.now().astimezone().isoformat(),None)); self.conn.commit()
    def agents(self):
        return [{"id":r["id"],"habitat_id":r["habitat_id"],"name":r["name"],"enabled":bool(r["enabled"]),"permissions":json.loads(r["permissions"]),"created_at":r["created_at"],"last_seen_at":r["last_seen_at"]} for r in self.conn.execute("SELECT * FROM agent ORDER BY name")]
    def authenticate_agent(self,agent_id,secret,permission):
        r=self.conn.execute("SELECT * FROM agent WHERE id=?",(agent_id,)).fetchone()
        if not r or not r["enabled"]: return False
        perms=json.loads(r["permissions"])
        if permission not in perms and "*" not in perms:return False
        if r["secret_hash"] and self.hash_secret(secret or "") != r["secret_hash"]:return False
        self.conn.execute("UPDATE agent SET last_seen_at=? WHERE id=?",(datetime.now().astimezone().isoformat(),agent_id)); self.conn.commit(); return True
