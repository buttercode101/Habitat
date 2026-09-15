#!/usr/bin/env python3
"""Standalone Habitat proof verifier.

This file intentionally uses only Python's standard library. Copy this single
file to a consumer machine and run:

    python verify_proof.py proof.json

It verifies structure, content integrity, and internal consistency. If a
signature is present it reports it as present-unverified because this verifier
does not ship cryptographic dependencies. Publisher trust and external-world
truth are never inferred from a bundle alone.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def date_time(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _validate_structure(bundle: dict[str, Any], errors: list[str]) -> None:
    allowed = {"proof_version", "generated_at", "claim", "ledger", "content_sha256", "signature"}
    required = {"proof_version", "generated_at", "claim", "ledger", "content_sha256"}
    unknown = sorted(set(bundle) - allowed)
    missing = sorted(required - set(bundle))
    if unknown:
        errors.append("unknown fields: " + ", ".join(unknown))
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if bundle.get("proof_version") != "1":
        errors.append("unsupported proof_version")
    if not date_time(bundle.get("generated_at")):
        errors.append("generated_at must be an ISO-8601 date-time")
    digest = bundle.get("content_sha256")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        errors.append("content_sha256 must be 64 lowercase hexadecimal characters")

    claim = bundle.get("claim")
    claim_required = {"id", "habitat_id", "job_id", "claim", "action", "expected_status", "created_at", "verified_at", "status", "evidence", "run_id"}
    if not isinstance(claim, dict):
        errors.append("claim must be an object")
    else:
        if set(claim) != claim_required:
            errors.append("claim has invalid fields")
        for field in ("id", "habitat_id", "claim", "expected_status", "status"):
            if not isinstance(claim.get(field), str):
                errors.append(f"claim.{field} must be a string")
        if not isinstance(claim.get("evidence"), dict):
            errors.append("claim.evidence must be an object")
        for field in ("job_id", "action", "run_id"):
            if claim.get(field) is not None and not isinstance(claim.get(field), str):
                errors.append(f"claim.{field} must be a string or null")
        if not date_time(claim.get("created_at")):
            errors.append("claim.created_at must be an ISO-8601 date-time")
        if claim.get("verified_at") is not None and not date_time(claim.get("verified_at")):
            errors.append("claim.verified_at must be an ISO-8601 date-time or null")

    ledger = bundle.get("ledger")
    if not isinstance(ledger, dict):
        errors.append("ledger must be an object")
    else:
        if set(ledger) != {"integrity", "actions"}:
            errors.append("ledger must contain exactly integrity and actions")
        if ledger.get("integrity") not in {"intact", "failed"}:
            errors.append("ledger.integrity must be 'intact' or 'failed'")
        actions = ledger.get("actions")
        if not isinstance(actions, list):
            errors.append("ledger.actions must be an array")
        else:
            required_action = {"id", "habitat_id", "job_id", "timestamp", "actor", "action", "status", "details", "run_id"}
            for index, action in enumerate(actions):
                if not isinstance(action, dict):
                    errors.append(f"ledger.actions[{index}] must be an object")
                    continue
                if set(action) != required_action:
                    errors.append(f"ledger.actions[{index}] has invalid fields")
                for field in ("id", "habitat_id", "actor", "action", "status"):
                    if not isinstance(action.get(field), str):
                        errors.append(f"ledger.actions[{index}].{field} must be a string")
                if not isinstance(action.get("details"), dict):
                    errors.append(f"ledger.actions[{index}].details must be an object")
                for field in ("job_id", "run_id"):
                    if action.get(field) is not None and not isinstance(action.get(field), str):
                        errors.append(f"ledger.actions[{index}].{field} must be a string or null")
                if not date_time(action.get("timestamp")):
                    errors.append(f"ledger.actions[{index}].timestamp must be an ISO-8601 date-time")

    if "signature" in bundle:
        signature = bundle["signature"]
        required_sig = {"algorithm", "key_id", "agent_id", "public_key", "signature"}
        if not isinstance(signature, dict) or set(signature) != required_sig:
            errors.append("signature has invalid fields")
        elif signature.get("algorithm") != "Ed25519":
            errors.append("signature.algorithm must be 'Ed25519'")
        elif any(signature.get(field) is not None and not isinstance(signature.get(field), str) for field in ("key_id", "agent_id")):
            errors.append("signature key_id and agent_id must be strings or null")
        elif not all(isinstance(signature.get(field), str) and signature.get(field) for field in ("public_key", "signature")):
            errors.append("signature public_key and signature must be non-empty strings")


def verify_proof(bundle: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    structure_errors: list[str] = []
    _validate_structure(bundle, structure_errors)
    errors.extend(structure_errors)

    expected = bundle.get("content_sha256")
    actual = None
    if isinstance(expected, str):
        digest_input = dict(bundle)
        digest_input.pop("generated_at", None)
        digest_input.pop("content_sha256", None)
        digest_input.pop("signature", None)
        actual = hashlib.sha256(canonical(digest_input).encode("utf-8")).hexdigest()
        if actual != expected:
            errors.append("content_sha256 mismatch")

    claim = bundle.get("claim")
    ledger = bundle.get("ledger")
    relationship_errors_before = len(errors)
    if isinstance(claim, dict) and isinstance(ledger, dict):
        actions = ledger.get("actions")
        if isinstance(actions, list):
            for index, action in enumerate(actions):
                if not isinstance(action, dict):
                    continue
                if action.get("habitat_id") != claim.get("habitat_id"):
                    errors.append(f"ledger.actions[{index}] habitat_id does not match claim")
                if claim.get("job_id") is not None and action.get("job_id") != claim.get("job_id"):
                    errors.append(f"ledger.actions[{index}] job_id does not match claim")
                if claim.get("run_id") is not None and action.get("run_id") != claim.get("run_id"):
                    errors.append(f"ledger.actions[{index}] run_id does not match claim")

            evidence = claim.get("evidence")
            if isinstance(evidence, dict) and evidence.get("action_id") is not None:
                action_id = evidence["action_id"]
                matched = next((a for a in actions if isinstance(a, dict) and a.get("id") == action_id), None)
                if matched is None:
                    errors.append("claim evidence action_id is absent from ledger.actions")
                else:
                    if claim.get("action") is not None and matched.get("action") != claim["action"]:
                        errors.append("claim evidence action does not match claim.action")
                    if claim.get("expected_status") is not None and matched.get("status") != claim["expected_status"]:
                        errors.append("claim evidence action status does not match claim.expected_status")
                    if claim.get("run_id") is not None and matched.get("run_id") != claim["run_id"]:
                        errors.append("claim evidence action run_id does not match claim.run_id")

    verdict = claim.get("status") if isinstance(claim, dict) else None
    integrity = ledger.get("integrity") if isinstance(ledger, dict) else None
    if verdict == "verified" and integrity != "intact":
        errors.append("verified claim cannot have failed ledger integrity")

    signature = bundle.get("signature")
    signature_state = "absent" if signature is None else "present-unverified"
    relationship_valid = len(errors) == relationship_errors_before
    content_valid = isinstance(actual, str) and actual == expected
    return {
        "valid": not errors,
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python verify_proof.py proof.json", file=sys.stderr)
        return 2
    try:
        with Path(sys.argv[1]).open("r", encoding="utf-8") as handle:
            bundle = json.load(handle)
        if not isinstance(bundle, dict):
            raise ValueError("proof bundle must be a JSON object")
        result = verify_proof(bundle)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
