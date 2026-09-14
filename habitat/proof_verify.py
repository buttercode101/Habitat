"""Dependency-free verification of exported Habitat proof bundles.

This verifier intentionally makes a narrow claim: it proves that the proof
bundle has not changed since its content digest was generated and that its
internal claim/ledger shape is coherent. It does not authenticate who created
the bundle or prove facts outside the evidence contained in the bundle.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def verify_proof(bundle: dict[str, Any]) -> dict[str, Any]:
    """Verify a decoded Habitat proof bundle without importing Habitat."""
    errors: list[str] = []
    required = {"proof_version", "claim", "ledger", "content_sha256"}
    missing = sorted(required - set(bundle))
    if missing:
        errors.append("missing fields: " + ", ".join(missing))

    claim = bundle.get("claim")
    ledger = bundle.get("ledger")
    if not isinstance(claim, dict):
        errors.append("claim must be an object")
    if not isinstance(ledger, dict):
        errors.append("ledger must be an object")

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

    integrity = ledger.get("integrity") if isinstance(ledger, dict) else None
    if integrity not in {"intact", "failed"}:
        errors.append("ledger.integrity must be 'intact' or 'failed'")

    verdict = claim.get("status") if isinstance(claim, dict) else None
    if verdict == "verified" and integrity != "intact":
        errors.append("verified claim cannot have failed ledger integrity")

    valid = not errors
    return {
        "valid": valid,
        "content_sha256": actual,
        "verdict": verdict,
        "ledger_integrity": integrity,
        "errors": errors,
        "scope": "bundle-integrity-and-internal-consistency",
        "authenticity": "not-established",
    }


def verify_file(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return verify_proof(json.load(handle))
