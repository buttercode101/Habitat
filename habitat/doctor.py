from __future__ import annotations
import os,sys
from .store import Store

def diagnose(db_path,config_path=None):
    checks=[]
    try:
        s=Store(db_path);h=s.habitat(); checks.append(('database',True,'SQLite readable'));checks.append(('schema',True,f'version {s.conn.execute("SELECT value FROM schema_meta WHERE key=\'version\'").fetchone()[0]}'));checks.append(('configuration',config_path is None or os.path.exists(config_path),'present' if config_path is None or os.path.exists(config_path) else 'missing'));checks.append(('jobs',True,f'{len(s.jobs())} configured'));checks.append(('agents',True,f'{len(s.agents())} registered'));s.close()
    except Exception as e:checks.append(('database',False,str(e)))
    checks.append(('python',sys.version_info>=(3,10),sys.version.split()[0]));checks.append(('signing_secret',True, 'set' if os.getenv('HABITAT_WEBHOOK_SECRET') else 'not set; configure HABITAT_WEBHOOK_SECRET before starting signed event ingestion'))
    return checks
