import json
from pathlib import Path

import habitat.__main__ as cli


def test_proof_command_exports_only_portable_bundle(tmp_path: Path, monkeypatch):
    proof = {
        "proof_version": "1",
        "claim": {"status": "verified"},
        "ledger": {"integrity": "intact", "actions": []},
        "content_sha256": "abc",
    }

    class FakeStore:
        def __init__(self, _db):
            pass

        def close(self):
            pass

    monkeypatch.setattr(cli, "Store", FakeStore)
    monkeypatch.setattr(cli, "proof_status", lambda _store, _id: {
        "claim_id": "c1",
        "verdict": "verified",
        "ledger_integrity": "intact",
        "content_sha256": "abc",
        "proof": proof,
    })

    output = tmp_path / "proof.json"
    assert cli.main(["--db", str(tmp_path / "db.sqlite"), "proof", "c1", "-o", str(output)]) == 0
    assert json.loads(output.read_text(encoding="utf-8")) == proof
