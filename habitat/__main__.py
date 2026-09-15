from __future__ import annotations
import argparse,json,os,sys,secrets
from pathlib import Path
from .schema import Habitat,Job,utcnow
from .store import Store
from .config import load_config,validate_config
from .runtime import run_once,run_loop
from .claims import Claim
from .verify import verify_claim
from .verify_api import proof_status,verify_and_prove
from .adapters import JSONFileEvidenceAdapter,HTTPJSONEvidenceAdapter,GitHubIssueEvidenceAdapter
from .events import signature_for,ingest_event
from .server import serve
from .generate import render_dashboard,write_dashboard
from .doctor import diagnose
from .backup import backup,restore
from .proof_sign import sign_proof
DEFAULT_DB=Path('.habitat/habitat.db')
def get_store(a):return Store(a.db)
def cmd_init(a):
    cfg=validate_config(load_config(a.config));s=Store(a.db);now=utcnow();s.save_habitat(Habitat(cfg['id'],cfg['name'],cfg.get('model','unknown'),now,now))
    for j in cfg.get('jobs',[]):s.save_job(Job(j['id'],cfg['id'],j['name'],j.get('schedule'),j.get('enabled',True),j.get('command')))
    s.close();print(f'Initialized Habitat {cfg["id"]} at {a.db}');return 0
def cmd_status(a):
    s=get_store(a);h=s.habitat();print(json.dumps({'id':h.id,'name':h.name,'status':h.status,'jobs':len(s.jobs()),'active_signals':len(s.active_signals()),'agents':len(s.agents())},indent=2));s.close();return 0
def cmd_run(a):
    s=get_store(a)
    try:
        if a.watch:run_loop(s,interval=a.interval,stop_after=a.duration)
        else:run_once(s)
    finally:s.close()
    return 0
def cmd_inspect(a):
    s=get_store(a);print(json.dumps({'habitat':s.habitat().__dict__,'jobs':[j.__dict__ for j in s.jobs()],'signals':[x.__dict__ for x in s.signals()]},default=str,indent=2));s.close();return 0
def cmd_claim(a):
    s=get_store(a);c=Claim.new(s.habitat().id,a.claim,a.job,a.action,a.expected_status);c.run_id=a.run_id;s.save_claim(c);print(json.dumps({'id':c.id,'status':c.status,'run_id':c.run_id,'claim':c.claim},default=str));s.close();return 0
def _evidence(a):
    if a.evidence_file:return JSONFileEvidenceAdapter(a.evidence_file)
    if a.evidence_url:return HTTPJSONEvidenceAdapter(a.evidence_url,a.token_env)
    if a.github_issue:return GitHubIssueEvidenceAdapter(a.token_env)
    return None
def cmd_verify(a):
    s=get_store(a);c=s.get_claim(a.id) if a.id else (s.claims(1)[0] if s.claims(1) else None)
    if not c:print('No claim found');s.close();return 1
    expected=json.loads(a.evidence_expected) if a.evidence_expected else None;c=verify_claim(s,c,_evidence(a),a.query or a.github_issue,expected);print(json.dumps({'id':c.id,'status':c.status,'evidence':c.evidence},default=str));s.close();return 0
def cmd_proof(a):
    s=get_store(a)
    try:
        result=verify_and_prove(s,a.id) if a.reverify else proof_status(s,a.id)
        proof=result['proof']
        if a.signing_key_env:
            private_key=os.getenv(a.signing_key_env)
            if not private_key:
                raise ValueError(f"Signing key environment variable is not set: {a.signing_key_env}")
            proof=sign_proof(proof,private_key,a.key_id,a.agent_id)
            result['proof']=proof
            result['signed']=True
        else:
            result['signed']=False
        if a.output:
            Path(a.output).write_text(json.dumps(proof,default=str,indent=2,sort_keys=True)+'\n',encoding='utf-8')
            print(f'Wrote proof to {a.output}')
        else:
            print(json.dumps(result,default=str,indent=2))
        return 0
    except KeyError:
        print(json.dumps({'error':'claim_not_found'}));return 1
    except (RuntimeError,ValueError) as exc:
        print(json.dumps({'error':str(exc)}));return 1
    finally:s.close()
def cmd_event(a):
    s=get_store(a)
    body=Path(a.file).read_bytes() if a.file else a.json.encode()
    secret=os.getenv(a.secret_env) if a.secret_env else None
    agent_secret=os.getenv(a.agent_secret_env) if a.agent_secret_env else None
    sig=a.signature or (signature_for(secret,body) if secret else None)
    try:print(json.dumps(ingest_event(s,body,sig,secret,not a.no_signature,a.agent_id,agent_secret),default=str));return 0
    except (ValueError,PermissionError) as e:print(json.dumps({'accepted':False,'error':str(e)}));return 1
    finally:s.close()
def cmd_agent_add(a):
    s=get_store(a);h=s.habitat();secret=os.getenv(a.secret_env) if a.secret_env else None
    secret=secret or secrets.token_urlsafe(32);s.save_agent(a.id,h.id,a.name,True,a.permission,secret);s.close();print(json.dumps({'agent_id':a.id,'secret':secret,'permissions':a.permission}));return 0
def cmd_agents(a):
    s=get_store(a);print(json.dumps(s.agents(),indent=2,default=str));s.close();return 0
def cmd_doctor(a):
    checks=diagnose(a.db,a.config);bad=False
    for n,ok,msg in checks:print(f'{"✓" if ok else "✗"} {n}: {msg}');bad|=not ok
    print('Result:', 'NEEDS ATTENTION' if bad else 'HEALTHY');return 1 if bad else 0
def cmd_backup(a):print(f'Backup written to {backup(a.db,a.output)}');return 0
def cmd_restore(a):print(f'Restored database to {restore(a.input,a.db)}');return 0
def cmd_generate(a):
    s=get_store(a);p=write_dashboard(render_dashboard(s.habitat(),s.jobs(),s.signals(),s.actions(),s.habitat().name),a.output);s.close();print(f'Wrote {p.resolve()}');return 0
def main(argv=None):
    p=argparse.ArgumentParser(prog='habitat',description='Local-first supervision and accountability runtime for autonomous agents.');p.add_argument('--db',default=str(DEFAULT_DB));sub=p.add_subparsers(dest='command',required=True)
    x=sub.add_parser('init');x.add_argument('--config',required=True);x.set_defaults(func=cmd_init)
    sub.add_parser('status').set_defaults(func=cmd_status)
    x=sub.add_parser('run');x.add_argument('--watch',action='store_true');x.add_argument('--interval',type=float,default=10);x.add_argument('--duration',type=float);x.set_defaults(func=cmd_run)
    sub.add_parser('inspect').set_defaults(func=cmd_inspect)
    x=sub.add_parser('generate');x.add_argument('-o','--output',default='dashboard.html');x.set_defaults(func=cmd_generate)
    x=sub.add_parser('claim');x.add_argument('claim');x.add_argument('--job');x.add_argument('--action');x.add_argument('--expected-status',default='ok');x.add_argument('--run-id');x.set_defaults(func=cmd_claim)
    x=sub.add_parser('verify');x.add_argument('--id');x.add_argument('--query');x.add_argument('--evidence-file');x.add_argument('--evidence-url');x.add_argument('--github-issue');x.add_argument('--token-env',default='GITHUB_TOKEN');x.add_argument('--evidence-expected');x.set_defaults(func=cmd_verify)
    x=sub.add_parser('proof');x.add_argument('id');x.add_argument('--reverify',action='store_true');x.add_argument('-o','--output',help='write only the portable proof bundle to this JSON file');x.add_argument('--signing-key-env',help='environment variable containing a base64 Ed25519 private key');x.add_argument('--key-id',help='trusted-key registry identifier to embed in the signature');x.add_argument('--agent-id',help='publisher agent identifier to bind into the signature');x.set_defaults(func=cmd_proof)
    x=sub.add_parser('event');x.add_argument('--file');x.add_argument('--json',default='');x.add_argument('--signature');x.add_argument('--secret-env',default='HABITAT_WEBHOOK_SECRET');x.add_argument('--agent-id');x.add_argument('--agent-secret-env',default='HABITAT_AGENT_SECRET');x.add_argument('--no-signature',action='store_true');x.set_defaults(func=cmd_event)
    x=sub.add_parser('agents');x.set_defaults(func=cmd_agents)
    x=sub.add_parser('agent-add');x.add_argument('id');x.add_argument('name');x.add_argument('--permission',action='append',default=['submit_events']);x.add_argument('--secret-env',default='HABITAT_AGENT_SECRET');x.set_defaults(func=cmd_agent_add)
    x=sub.add_parser('doctor');x.add_argument('--config');x.set_defaults(func=cmd_doctor)
    x=sub.add_parser('backup');x.add_argument('output');x.set_defaults(func=cmd_backup)
    x=sub.add_parser('restore');x.add_argument('input');x.set_defaults(func=cmd_restore)
    x=sub.add_parser('serve');x.add_argument('--host',default='127.0.0.1');x.add_argument('--port',type=int,default=8787);x.add_argument('--secret-env',default='HABITAT_WEBHOOK_SECRET');x.add_argument('--allow-unsigned',action='store_true');x.set_defaults(func=lambda a:serve(a.db,a.host,a.port,os.getenv(a.secret_env),not a.allow_unsigned))
    args=p.parse_args(argv); return args.func(args)
if __name__=='__main__':sys.exit(main(argv=None))