"""Local-first Habitat HTTP API."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse
from .events import ingest_event,MAX_EVENT_BYTES
from .store import Store
from .generate import render_dashboard
from .verify_api import proof_status, verify_and_prove

def make_handler(db_path,secret,require_signature=True):
    class Handler(BaseHTTPRequestHandler):
        server_version='Habitat/1.1'
        def _send(self,code,payload):
            raw=json.dumps(payload,default=str).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
        def do_GET(self):
            path=urlparse(self.path).path; s=Store(db_path)
            try:
                if path in ('/','/dashboard'):
                    html=render_dashboard(s.habitat(),s.jobs(),s.signals(),s.actions(),s.habitat().name);raw=html.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
                elif path=='/v1/status':
                    h=s.habitat();self._send(200,{'id':h.id,'name':h.name,'status':h.status,'model':h.model,'jobs':len(s.jobs()),'active_signals':len(s.active_signals()),'agents':len(s.agents())})
                elif path=='/v1/claims':self._send(200,[c.__dict__ for c in s.claims()])
                elif path.startswith('/v1/claims/') and path.endswith('/proof'):
                    claim_id=path[len('/v1/claims/'):-len('/proof')].strip('/')
                    if not claim_id:self._send(400,{'error':'missing_claim_id'})
                    else:self._send(200,proof_status(s,claim_id))
                elif path.startswith('/v1/claims/') and path.endswith('/verify'):
                    claim_id=path[len('/v1/claims/'):-len('/verify')].strip('/')
                    if not claim_id:self._send(400,{'error':'missing_claim_id'})
                    else:self._send(200,verify_and_prove(s,claim_id))
                elif path=='/v1/signals':self._send(200,[x.__dict__ for x in s.active_signals()])
                elif path=='/v1/events':self._send(200,s.events())
                elif path=='/v1/actions':self._send(200,[x.__dict__ for x in s.actions()])
                elif path=='/v1/agents':self._send(200,s.agents())
                elif path=='/healthz':self._send(200,{'ok':True})
                else:self._send(404,{'error':'not_found'})
            except KeyError:self._send(404,{'error':'claim_not_found'})
            except RuntimeError as e:self._send(503,{'error':str(e)})
            finally:s.close()
        def do_POST(self):
            if urlparse(self.path).path!='/v1/events':self._send(404,{'error':'not_found'});return
            try:length=int(self.headers.get('Content-Length','0'))
            except ValueError:self._send(400,{'error':'invalid_content_length'});return
            if length<=0 or length>MAX_EVENT_BYTES:self._send(413,{'error':'event_too_large'});return
            body=self.rfile.read(length);sig=self.headers.get('X-Habitat-Signature');agent_id=self.headers.get('X-Habitat-Agent');agent_secret=self.headers.get('X-Habitat-Agent-Secret');s=Store(db_path)
            try:
                result=ingest_event(s,body,sig,secret,require_signature,agent_id,agent_secret or secret);self._send(200 if result.get('duplicate') else 202,result)
            except PermissionError as e:self._send(401,{'error':str(e)})
            except ValueError as e:self._send(400,{'error':str(e)})
            finally:s.close()
        def log_message(self,*args):return
    return Handler

def serve(db_path,host='127.0.0.1',port=8787,secret=None,require_signature=True):
    httpd=ThreadingHTTPServer((host,port),make_handler(db_path,secret,require_signature));print(f'Habitat API listening on http://{host}:{port}')
    try:httpd.serve_forever()
    except KeyboardInterrupt:pass
    finally:httpd.server_close()
