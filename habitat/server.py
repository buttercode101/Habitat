"""Local-first Habitat HTTP API.

The API is intentionally safe-by-default for local use. Loopback listeners may
be used without an HTTP auth header; non-loopback listeners require the
configured server secret as a bearer credential for every request.
"""
from __future__ import annotations

import hmac
import ipaddress
import json
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .events import ingest_event, MAX_EVENT_BYTES
from .store import Store
from .generate import render_dashboard
from .verify_api import proof_status, verify_and_prove


def _is_loopback_host(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host.lower() in {"localhost", "ip6-localhost"}


def make_handler(db_path, secret, require_signature=True, protect_remote=True):
    class Handler(BaseHTTPRequestHandler):
        server_version = "Habitat/1.3"
        protocol_version = "HTTP/1.1"

        def _remote_protected(self) -> bool:
            if not protect_remote:
                return False
            bound = getattr(self.server, "server_address", ("127.0.0.1", 0))[0]
            return not _is_loopback_host(str(bound))

        def _authorized_read(self) -> bool:
            if not self._remote_protected():
                return True
            supplied = self.headers.get("Authorization", "")
            if not secret or not supplied.startswith("Bearer "):
                return False
            return hmac.compare_digest(supplied[7:].strip(), secret)

        def _send(self, code, payload):
            raw = json.dumps(payload, default=str).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(raw)

        def _send_forbidden(self):
            self._send(401, {"error": "authentication_required"})

        def do_GET(self):
            if not self._authorized_read():
                self._send_forbidden()
                return
            path = urlparse(self.path).path
            s = Store(db_path)
            try:
                if path in ("/", "/dashboard"):
                    html = render_dashboard(s.habitat(), s.jobs(), s.signals(), s.actions(), s.habitat().name)
                    raw = html.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(raw)))
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.send_header("Referrer-Policy", "no-referrer")
                    self.end_headers()
                    self.wfile.write(raw)
                elif path == "/v1/status":
                    h = s.habitat()
                    self._send(200, {"id": h.id, "name": h.name, "status": h.status, "model": h.model, "jobs": len(s.jobs()), "active_signals": len(s.active_signals()), "agents": len(s.agents())})
                elif path == "/v1/claims":
                    self._send(200, [c.__dict__ for c in s.claims()])
                elif path.startswith("/v1/claims/") and path.endswith("/proof"):
                    claim_id = path[len("/v1/claims/"):-len("/proof")].strip("/")
                    if not claim_id:
                        self._send(400, {"error": "missing_claim_id"})
                    else:
                        self._send(200, proof_status(s, claim_id))
                elif path.startswith("/v1/claims/") and path.endswith("/verify"):
                    claim_id = path[len("/v1/claims/"):-len("/verify")].strip("/")
                    if not claim_id:
                        self._send(400, {"error": "missing_claim_id"})
                    else:
                        self._send(200, verify_and_prove(s, claim_id))
                elif path == "/v1/signals":
                    self._send(200, [x.__dict__ for x in s.active_signals()])
                elif path == "/v1/events":
                    self._send(200, s.events())
                elif path == "/v1/actions":
                    self._send(200, [x.__dict__ for x in s.actions()])
                elif path == "/v1/agents":
                    self._send(200, s.agents())
                elif path == "/healthz":
                    self._send(200, {"ok": True})
                else:
                    self._send(404, {"error": "not_found"})
            except KeyError:
                self._send(404, {"error": "claim_not_found"})
            except RuntimeError as exc:
                self._send(503, {"error": str(exc)})
            finally:
                s.close()

        def do_POST(self):
            if urlparse(self.path).path != "/v1/events":
                self._send(404, {"error": "not_found"})
                return
            if self._remote_protected() and not self._authorized_read():
                self._send_forbidden()
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send(400, {"error": "invalid_content_length"})
                return
            if length <= 0 or length > MAX_EVENT_BYTES:
                self._send(413, {"error": "event_too_large"})
                return
            self.connection.settimeout(10)
            body = self.rfile.read(length)
            if len(body) != length:
                self._send(400, {"error": "incomplete_request_body"})
                return
            sig = self.headers.get("X-Habitat-Signature")
            agent_id = self.headers.get("X-Habitat-Agent")
            agent_secret = self.headers.get("X-Habitat-Agent-Secret")
            s = Store(db_path)
            try:
                result = ingest_event(s, body, sig, secret, require_signature, agent_id, agent_secret)
                self._send(200 if result.get("duplicate") else 202, result)
            except PermissionError as exc:
                self._send(401, {"error": str(exc)})
            except ValueError as exc:
                self._send(400, {"error": str(exc)})
            finally:
                s.close()

        def log_message(self, *args):
            return

    return Handler


def serve(db_path, host="127.0.0.1", port=8787, secret=None, require_signature=True):
    if not _is_loopback_host(host) and not secret:
        raise ValueError("non-loopback listeners require a server secret")
    class HabitatHTTPServer(ThreadingHTTPServer):
        allow_reuse_address = True
        daemon_threads = True
    httpd = HabitatHTTPServer((host, port), make_handler(db_path, secret, require_signature, protect_remote=True))
    print(f"Habitat API listening on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
