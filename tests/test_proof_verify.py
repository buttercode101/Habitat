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


def _digest(bundle):
    import hashlib, json
    d = dict(bundle)
    d.pop("generated_at", None)
    d.pop("content_sha256", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def test_standalone_verifier_accepts_valid_bundle():
    result = verify_proof(_bundle())
    assert result["valid"] is True
    assert result["verdict"] == "verified"
    assert result["authenticity"] == "not-established"
    assert result["assurance"] == {
        "structural_validity": True,
        "content_integrity": True,
        "internal_consistency": True,
        "signature": "absent",
        "publisher_trust": "not-assessed",
        "external_truth": "not-established",
    }


def test_present_signature_is_not_mistaken_for_verified_authenticity():
    bundle = _bundle()
    bundle["signature"] = {
        "algorithm": "Ed25519",
        "key_id": "k1",
        "agent_id": "a1",
        "public_key": "public",
        "signature": "signature",
    }
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is True
    assert result["assurance"]["signature"] == "present-unverified"
    assert result["assurance"]["publisher_trust"] == "not-assessed"
    assert result["external_truth"] if "external_truth" in result else True


def test_standalone_verifier_rejects_modified_bundle():
    bundle = _bundle()
    bundle["claim"]["status"] = "failed"
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "content_sha256 mismatch" in result["errors"]


def test_verified_cannot_claim_failed_ledger():
    bundle = _bundle()
    bundle["ledger"]["integrity"] = "failed"
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "verified claim cannot have failed ledger integrity" in result["errors"]


def test_verifier_rejects_cross_habitat_action_even_with_fresh_digest():
    bundle = _bundle()
    bundle["claim"] = {
        "id": "c1", "habitat_id": "h1", "job_id": "j1", "action": "deploy",
        "expected_status": "ok", "status": "verified", "evidence": {"action_id": "a1"}
    }
    bundle["ledger"]["actions"] = [{
        "id": "a1", "habitat_id": "h2", "job_id": "j1", "action": "deploy",
        "status": "ok", "run_id": "r1"
    }]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "ledger.actions[0] habitat_id does not match claim" in result["errors"]


def test_verifier_rejects_cross_run_evidence_even_with_fresh_digest():
    bundle = _bundle()
    bundle["claim"] = {
        "id": "c1", "habitat_id": "h1", "job_id": "j1", "action": "deploy",
        "expected_status": "ok", "status": "verified", "run_id": "r1",
        "evidence": {"action_id": "a1"}
    }
    bundle["ledger"]["actions"] = [{
        "id": "a1", "habitat_id": "h1", "job_id": "j1", "action": "deploy",
        "status": "ok", "run_id": "r2"
    }]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "ledger.actions[0] run_id does not match claim" in result["errors"]


def test_verifier_rejects_evidence_action_mismatch():
    bundle = _bundle()
    bundle["claim"] = {
        "id": "c1", "habitat_id": "h1", "job_id": "j1", "action": "deploy",
        "expected_status": "ok", "status": "verified", "run_id": "r1",
        "evidence": {"action_id": "a1"}
    }
    bundle["ledger"]["actions"] = [{
        "id": "a1", "habitat_id": "h1", "job_id": "j1", "action": "restart",
        "status": "ok", "run_id": "r1"
    }]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "claim evidence action does not match claim.action" in result["errors"]


def test_verifier_accepts_valid_correlated_evidence():
    bundle = _bundle()
    bundle["claim"] = {
        "id": "c1", "habitat_id": "h1", "job_id": "j1", "action": "deploy",
        "expected_status": "ok", "status": "verified", "run_id": "r1",
        "evidence": {"action_id": "a1"}
    }
    bundle["ledger"]["actions"] = [{
        "id": "a1", "habitat_id": "h1", "job_id": "j1", "action": "deploy",
        "status": "ok", "run_id": "r1"
    }]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is True
