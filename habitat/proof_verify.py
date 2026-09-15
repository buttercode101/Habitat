"""Dependency-free verification of exported Habitat proof bundles.

This verifier intentionally makes a narrow claim: it proves that the proof
bundle has not changed since its content digest was generated and that its
internal claim/ledger relationships are coherent. It does not authenticate
who created the bundle or prove facts outside the evidence contained in it.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate_structure(bundle: dict[str, Any], errors: list[str]) -> bool:
    required = {"proof_version", "claim", "ledger", "content_sha256"}
    missing = sorted(required - set(bundle))
    if missing:
        errors.append("missing fields: " + ", ".join(missing))

    if bundle.get("proof_version") != "1":
        errors.append("unsupported proof_version")

    claim = bundle.get("claim")
    ledger = bundle.get("ledger")
    if not isinstance(claim, dict):
        errors.append("claim must be an object")
    if not isinstance(ledger, dict):
        errors.append("ledger must be an object")
    if not isinstance(bundle.get("content_sha256"), str):
        errors.append("content_sha256 must be a string")

    if isinstance(ledger, dict):
        if ledger.get("integrity") not in {"intact", "failed"}:
            errors.append("ledger.integrity must be 'intact' or 'failed'")
        if not isinstance(ledger.get("actions"), list):
            errors.append("ledger.actions must be an array")

    if isinstance(bundle.get("signature"), dict):
        signature = bundle["signature"]
        if signature.get("algorithm") != "Ed25519":
            errors.append("signature.algorithm must be 'Ed25519'")
        for field in ("key_id", "agent_id", "public_key", "signature"):
            if field not in signature:
                errors.append(f"signature.{field} is required")
    elif "signature" in bundle:
        errors.append("signature must be an object")

    return not errors


def _validate_relationships(claim: dict[str, Any], ledger: dict[str, Any], errors: list[str]) -> None:
    actions = ledger.get("actions")
    if not isinstance(actions, list):
        return

    claim_habitat = claim.get("habitat_id")
    claim_job = claim.get("job_id")
    claim_run = claim.get("run_id")
    claim_action = claim.get("action")
    expected_status = claim.get("expected_status")

    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            errors.append(f"ledger.actions[{index}] must be an object")
            continue
        if claim_habitat is not None and action.get("habitat_id") != claim_habitat:
            errors.append(f"ledger.actions[{index}] habitat_id does not match claim")
        if claim_job is not None and action.get("job_id") != claim_job:
            errors.append(f"ledger.actions[{index}] job_id does not match claim")
        if claim_run is not None and action.get("run_id") != claim_run:
            errors.append(f"ledger.actions[{index}] run_id does not match claim")

    evidence = claim.get("evidence")
    if not isinstance(evidence, dict):
        return
    evidence_action_id = evidence.get("action_id")
    if evidence_action_id is None:
        return

    matched = next((a for a in actions if isinstance(a, dict) and a.get("id") == evidence_action_id), None)
    if matched is None:
        errors.append("claim evidence action_id is absent from ledger.actions")
        return
    if claim_action is not None and matched.get("action") != claim_action:
        errors.append("claim evidence action does not match claim.action")
    if expected_status is not None and matched.get("status") != expected_status:
        errors.append("claim evidence action status does not match claim.expected_status")
    if claim_run is not None and matched.get("run_id") != claim_run:
        errors.append("claim evidence action run_id does not match claim.run_id")


def verify_proof(bundle: dict[str, Any]) -> dict[str, Any]:
    """Verify a decoded Habitat proof bundle and report assurance boundaries."""
    errors: list[str] = []
    structure_errors: list[str] = []
    _validate_structure(bundle, structure_errors)
    errors.extend(structure_errors)

    expected = bundle.get("content_sha256")
    if isinstance(expected, str):
        digest_input = dict(bundle)
        digest_input.pop("generated_at", None)
        # The digest authenticates the bundle contents, excluding the digest
        # field itself to avoid a circular hash.
        digest_input.pop("content_sha256", None)
        actual = hashlib.sha256(_canonical(digest_input).encode()).hexdigest()
        if actual != expected:
            errors.append("content_sha256 mismatch")
    else:
        actual = None

    claim = bundle.get("claim")
    ledger = bundle.get("ledger")
    relationship_errors_before = len(errors)
    if isinstance(claim, dict) and isinstance(ledger, dict):
        _validate_relationships(claim, ledger, errors)

    verdict = claim.get("status") if isinstance(claim, dict) else None
    integrity = ledger.get("integrity") if isinstance(ledger, dict) else None
    if verdict == "verified" and integrity != "intact":
        errors.append("verified claim cannot have failed ledger integrity")

    relationship_valid = len(errors) == relationship_errors_before
    content_valid = isinstance(actual, str) and actual == expected
    signature = bundle.get("signature")
    signature_state = "absent" if signature is None else "present-unverified"

    valid = not errors
    return {
        "valid": valid,
        "content_sha256": actual,
        "verdict": verdict,
        "ledger_integrity": integrity,
        "errors": errors,
        "scope": "bundle-integrity-and-internal-consistency",
        "authenticity": "not-established",
        "assurance": {
            "structural_validity": not structure_errors,
            "content_integrity": content_valid,
            "internal_consistency": relationship_valid and not (verdict == "verified" and integrity != "intact"),
            "signature": signature_state,
            "publisher_trust": "not-assessed",
            "external_truth": "not-established",
        },
    }


def verify_file(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return verify_proof(json.load(handle))
