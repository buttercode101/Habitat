"""Integration boundaries for Habitat runtimes and evidence sources.

Adapters are intentionally small and stdlib-only. They let Habitat verify claims
against systems outside its own process without making those systems part of the
core domain model.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import subprocess
import shlex
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

@dataclass
class ExecutionResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None

class JobAdapter(Protocol):
    def execute(self, command: str, timeout: int = 300) -> ExecutionResult: ...

class ShellAdapter:
    """Local command adapter. Safe argv execution is the default; shell mode is explicit."""
    def __init__(self, allow_shell: bool = False): self.allow_shell = allow_shell
    def execute(self, command: str, timeout: int = 300) -> ExecutionResult:
        try:
            argv = command if self.allow_shell else shlex.split(command)
            p = subprocess.run(argv, shell=self.allow_shell, capture_output=True, text=True, timeout=timeout)
            return ExecutionResult(p.returncode == 0, p.stdout[-4000:], p.stderr[-4000:], p.returncode)
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(False, str(exc.stdout or "")[-4000:], "command timed out", None)
        except Exception as exc:
            return ExecutionResult(False, "", str(exc)[-4000:], None)

@dataclass
class Evidence:
    """Normalized evidence returned by an external system."""
    source: str
    observed: bool
    status: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

class EvidenceAdapter(Protocol):
    def observe(self, query: str) -> Evidence: ...

class JSONFileEvidenceAdapter:
    """Read deterministic evidence from a local JSON document."""
    def __init__(self, path: str | Path): self.path = Path(path)
    def observe(self, query: str) -> Evidence:
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8")); value: Any = payload
            for part in query.split(".") if query else []:
                if not isinstance(value, dict) or part not in value: return Evidence(str(self.path), False, error=f"path_not_found:{query}")
                value = value[part]
            if isinstance(value, dict): return Evidence(str(self.path), True, value.get("status"), value)
            return Evidence(str(self.path), True, str(value) if value is not None else None, {"value": value})
        except Exception as exc: return Evidence(str(self.path), False, error=str(exc))

class HTTPJSONEvidenceAdapter:
    """Fetch JSON evidence from an HTTP endpoint."""
    def __init__(self, base_url: str, token_env: str | None = None, timeout: int = 15):
        self.base_url = base_url.rstrip("/"); self.token_env = token_env; self.timeout = timeout
    def observe(self, query: str) -> Evidence:
        req = Request(self.base_url, headers={"Accept": "application/json", "User-Agent": "Habitat/1.0"}); token = os.getenv(self.token_env) if self.token_env else None
        if token: req.add_header("Authorization", f"Bearer {token}")
        try:
            with urlopen(req, timeout=self.timeout) as response: payload = json.loads(response.read().decode("utf-8"))
            value: Any = payload
            for part in query.split(".") if query else []:
                if not isinstance(value, dict) or part not in value: return Evidence(self.base_url, False, error=f"path_not_found:{query}")
                value = value[part]
            if isinstance(value, dict): return Evidence(self.base_url, True, value.get("status"), value)
            return Evidence(self.base_url, True, str(value) if value is not None else None, {"value": value})
        except HTTPError as exc: return Evidence(self.base_url, False, error=f"http_{exc.code}")
        except (URLError, TimeoutError, ValueError) as exc: return Evidence(self.base_url, False, error=str(exc))

class GitHubIssueEvidenceAdapter:
    """Verify that a GitHub issue exists. Query format: owner/repo#number."""
    def __init__(self, token_env: str = "GITHUB_TOKEN", timeout: int = 15): self.token_env = token_env; self.timeout = timeout
    def observe(self, query: str) -> Evidence:
        try:
            repo, number = query.rsplit("#", 1); owner, name = repo.split("/", 1); url = f"https://api.github.com/repos/{owner}/{name}/issues/{int(number)}"
            req = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "Habitat/1.0"}); token = os.getenv(self.token_env)
            if token: req.add_header("Authorization", f"Bearer {token}")
            with urlopen(req, timeout=self.timeout) as response: payload = json.loads(response.read().decode("utf-8"))
            return Evidence("github", True, "ok", {"number": payload.get("number"), "state": payload.get("state"), "title": payload.get("title"), "url": payload.get("html_url")})
        except HTTPError as exc:
            if exc.code == 404: return Evidence("github", False, error="issue_not_found")
            return Evidence("github", False, error=f"http_{exc.code}")
        except (ValueError, URLError, TimeoutError) as exc: return Evidence("github", False, error=str(exc))
