from habitat.proof_verify import MAX_PROOF_ACTIONS, verify_proof


def _bundle():
    import hashlib, json
    b = {
        "proof_version": "1",
        "generated_at": "2026-01-01T00:00:00+00:00",
        "claim": {
            "id": "c1", "habitat_id": "h1", "job_id": None, "claim": "x",
            "action": None, "expected_status": "ok", "created_at": "2026-01-01T00:00:00+00:00",
            "verified_at": "2026-01-01T00:00:01+00:00", "status": "verified", "evidence": {}, "run_id": None,
        },
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
    d.pop("signature", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _action(habitat="h1", job="j1", action="deploy", status="ok", run="r1"):
    return {"id": "a1", "habitat_id": habitat, "job_id": job, "timestamp": "2026-01-01T00:00:00+00:00", "actor": "agent", "action": action, "status": status, "details": {}, "run_id": run}


def test_verifier_accepts_valid_bundle_with_explicit_assurance_levels():
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
        "algorithm": "Ed25519", "key_id": "k1", "agent_id": "a1",
        "public_key": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
        "signature": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==",
    }
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["assurance"]["signature"] in {"present-unverified", "invalid"}
    if result["assurance"]["signature"] == "present-unverified":
        assert result["valid"] is True
    else:
        assert result["valid"] is False
    assert result["assurance"]["publisher_trust"] == "not-assessed"
    assert result["assurance"]["external_truth"] == "not-established"


def test_verifier_rejects_modified_bundle():
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
    bundle["claim"].update({"habitat_id": "h1", "job_id": "j1", "action": "deploy", "expected_status": "ok", "run_id": "r1", "evidence": {"action_id": "a1"}})
    bundle["ledger"]["actions"] = [_action(habitat="h2")]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "ledger.actions[0] habitat_id does not match claim" in result["errors"]


def test_verifier_rejects_cross_run_evidence_even_with_fresh_digest():
    bundle = _bundle()
    bundle["claim"].update({"habitat_id": "h1", "job_id": "j1", "action": "deploy", "expected_status": "ok", "run_id": "r1", "evidence": {"action_id": "a1"}})
    bundle["ledger"]["actions"] = [_action(run="r2")]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "ledger.actions[0] run_id does not match claim" in result["errors"]


def test_verifier_rejects_evidence_action_mismatch():
    bundle = _bundle()
    bundle["claim"].update({"habitat_id": "h1", "job_id": "j1", "action": "deploy", "expected_status": "ok", "run_id": "r1", "evidence": {"action_id": "a1"}})
    bundle["ledger"]["actions"] = [_action(action="restart")]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "claim evidence action does not match claim.action" in result["errors"]


def test_verifier_accepts_valid_correlated_evidence():
    bundle = _bundle()
    bundle["claim"].update({"habitat_id": "h1", "job_id": "j1", "action": "deploy", "expected_status": "ok", "run_id": "r1", "evidence": {"action_id": "a1"}})
    bundle["ledger"]["actions"] = [_action()]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is True


def test_verifier_rejects_unknown_top_level_fields():
    bundle = _bundle()
    bundle["trusted"] = True
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "unknown fields: trusted" in result["errors"]


def test_verifier_rejects_naive_datetime():
    bundle = _bundle()
    bundle["generated_at"] = "2026-01-01T00:00:00"
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "generated_at must be an ISO-8601 date-time with timezone" in result["errors"]


def test_verifier_rejects_non_finite_number():
    bundle = _bundle()
    bundle["claim"]["evidence"] = {"value": float("nan")}
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert "non-finite JSON numbers are not allowed" in result["errors"]


def test_verifier_bounds_action_count():
    bundle = _bundle()
    action = _action()
    bundle["ledger"]["actions"] = [dict(action, id=f"a{i}") for i in range(MAX_PROOF_ACTIONS + 1)]
    bundle["content_sha256"] = _digest(bundle)
    result = verify_proof(bundle)
    assert result["valid"] is False
    assert f"ledger.actions exceeds maximum of {MAX_PROOF_ACTIONS}" in result["errors"]
