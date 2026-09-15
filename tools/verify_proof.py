#!/usr/bin/env python3
"""Standalone Habitat proof verifier.

This file intentionally uses only Python's standard library. Copy this single
file to a consumer machine and run:

    python verify_proof.py proof.json

It verifies bundle structure, content integrity, and internal consistency. It
reports a present signature as unverified because the zero-install verifier
does not ship a cryptography implementation. Publisher trust and external
world truth are never inferred from a bundle alone.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate_structure(bundle: dict[str, Any], errors: list[str]) -> None:
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
        actual = hashlib.sha256(canonical(digest_input).encode()).hexdigest()
        if actual != expected:
            errors.append("content_sha256 mismatch")

    integrity = bundle.get("ledger", {}).get("integrity") if isinstance(bundle.get("ledger"), dict) else None
    claim = bundle.get("claim")
    ledger = bundle.get("ledger")
    relationship_errors_before = len(errors)
    if isinstance(claim, dict) and isinstance(ledger, dict):
        actions = ledger.get("actions")
        if isinstance(actions, list):
            for index, action in enumerate(actions):
                if not isinstance(action, dict):
                    errors.append(f"ledger.actions[{index}] must be an object")
                    continue
                for field in ("habitat_id", "job_id", "run_id"):
                    expected_value = claim.get(field)
                    if expected_value is not None and action.get(field) != expected_value:
                        errors.append(f"ledger.actions[{index}] {field} does not match claim")

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
    if verdict == "verified" and integrity != "intact":
        errors.append("verified claim cannot have failed ledger integrity")

    relationship_valid = len(errors) == relationship_errors_before
    content_valid = isinstance(actual, str) and actual == expected
    signature = bundle.get("signature")
    signature_state = "absent" if signature is None else "present-unverified"

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
