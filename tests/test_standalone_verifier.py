import json
import subprocess
import sys
from pathlib import Path

from habitat.proof_verify import verify_proof


ROOT = Path(__file__).resolve().parents[1]
STANDALONE = ROOT / "tools" / "verify_proof.py"


def _bundle():
    import hashlib

    bundle = {
        "proof_version": "1",
        "generated_at": "2026-01-01T00:00:00+00:00",
        "claim": {
            "id": "c1",
            "habitat_id": "h1",
            "job_id": "j1",
            "action": "deploy",
            "expected_status": "ok",
            "status": "verified",
            "run_id": "r1",
            "evidence": {"action_id": "a1"},
        },
        "ledger": {
            "integrity": "intact",
            "actions": [
                {
                    "id": "a1",
                    "habitat_id": "h1",
                    "job_id": "j1",
                    "action": "deploy",
                    "status": "ok",
                    "run_id": "r1",
                }
            ],
        },
    }
    digest_input = dict(bundle)
    digest_input.pop("generated_at")
    bundle["content_sha256"] = hashlib.sha256(
        json.dumps(digest_input, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    return bundle


def _run_standalone(bundle, tmp_path):
    path = tmp_path / "proof.json"
    path.write_text(json.dumps(bundle), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(STANDALONE), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout)


def test_standalone_matches_canonical_on_valid_bundle(tmp_path):
    bundle = _bundle()
    canonical = verify_proof(bundle)
    code, standalone = _run_standalone(bundle, tmp_path)

    assert code == 0
    assert standalone == canonical


def test_standalone_matches_canonical_on_tampered_bundle(tmp_path):
    bundle = _bundle()
    bundle["claim"]["action"] = "delete"
    canonical = verify_proof(bundle)
    code, standalone = _run_standalone(bundle, tmp_path)

    assert code == 1
    assert standalone == canonical
