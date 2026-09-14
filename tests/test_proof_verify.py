from habitat.proof_verify import verify_proof


def _bundle():
    import hashlib, json
    b = {
        "proof_version": "1",
        "generated_at": "2026-01-01T00:00:00+00:00",
        "claim": {"id": "c1", "status": "verified"},
        "ledger": {"integrity": "intact", "actions": []},
    }
    d = dict(b)
    d.pop("generated_at")
    b["content_sha256"] = hashlib.sha256(json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return b


def test_standalone_verifier_accepts_valid_bundle():
    result = verify_proof(_bundle())
    assert result["valid"] is True
    assert result["verdict"] == "verified"
    assert result["authenticity"] == "not-established"


def test_standalone_verifier_rejects_modified_bundle():
    bundle = _bundle()
    bundle["claim"]["status"] = "failed"
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "content_sha256 mismatch" in result["errors"]


def test_verified_cannot_claim_failed_ledger():
    bundle = _bundle()
    bundle["ledger"]["integrity"] = "failed"
    import hashlib, json
    d = dict(bundle)
    d.pop("generated_at")
    bundle["content_sha256"] = hashlib.sha256(json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "verified claim cannot have failed ledger integrity" in result["errors"]
