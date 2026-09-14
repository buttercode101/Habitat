from __future__ import annotations
import os, sys
from .store import Store

def diagnose(db_path, config_path=None):
    checks = []
    try:
        s = Store(db_path)
        s.habitat()
        version = s.conn.execute("SELECT value FROM schema_meta WHERE key='version'").fetchone()[0]
        checks.append(('database', True, 'SQLite readable'))
        checks.append(('schema', True, f'version {version}'))
        config_ok = config_path is None or os.path.exists(config_path)
        checks.append(('configuration', config_ok, 'present' if config_ok else 'missing'))
        checks.append(('jobs', True, f'{len(s.jobs())} configured'))
        checks.append(('agents', True, f'{len(s.agents())} registered'))
        s.close()
    except Exception as exc:
        checks.append(('database', False, str(exc)))
    checks.append(('python', sys.version_info >= (3, 10), sys.version.split()[0]))
    checks.append(('signing_secret', True, 'set' if os.getenv('HABITAT_WEBHOOK_SECRET') else 'not set; configure HABITAT_WEBHOOK_SECRET before starting signed event ingestion'))
    return checks
