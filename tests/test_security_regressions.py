import json

import pytest

from habitat.events import ingest_event, signature_for
from habitat.schema import Habitat, Job
from habitat.store import PBKDF2_ITERATIONS, Store


def make(tmp_path):
    store = Store(tmp_path / "security.db")
    store.save_habitat(Habitat("h", "H"))
    store.save_job(Job("j", "h", "J", enabled=True, command="echo ok"))
    return store


def test_agent_secret_uses_salted_slow_hash(tmp_path):
    store = make(tmp_path)
    store.save_agent("a", "h", "A", True, ["submit_events"], "correct-secret")
    row = store.conn.execute("SELECT secret_hash FROM agent WHERE id='a'").fetchone()
    stored = row[0]
    assert stored.startswith("pbkdf2_sha256$")
    assert f"${PBKDF2_ITERATIONS}$" in stored
    assert stored != Store.hash_secret("correct-secret")
    assert store.authenticate_agent("a", "correct-secret", "submit_events") is True
    assert store.authenticate_agent("a", "wrong-secret", "submit_events") is False
    store.close()


def test_legacy_sha256_agent_secret_is_upgraded_on_success(tmp_path):
    store = make(tmp_path)
    import hashlib

    legacy = hashlib.sha256(b"legacy-secret").hexdigest()
    store.conn.execute(
        "INSERT INTO agent VALUES (?,?,?,?,?,?,?,?)",
        ("legacy", "h", "Legacy", 1, json.dumps(["submit_events"]), legacy, "2026-01-01T00:00:00+00:00", None),
    )
    store.conn.commit()
    assert store.authenticate_agent("legacy", "legacy-secret", "submit_events") is True
    upgraded = store.conn.execute("SELECT secret_hash FROM agent WHERE id='legacy'").fetchone()[0]
    assert upgraded.startswith("pbkdf2_sha256$")
    assert upgraded != legacy
    store.close()


def test_non_standard_json_numbers_are_rejected(tmp_path):
    store = make(tmp_path)
    body = b'{"id":"nan-1","type":"job.completed","habitat_id":"h","job_id":"j","run_id":NaN}'
    with pytest.raises(ValueError, match="invalid_json"):
        ingest_event(store, body, signature_for("secret", body), "secret")
    store.close()
