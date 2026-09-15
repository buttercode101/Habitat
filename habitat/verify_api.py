"""Machine-consumable claim verification and portable proof responses."""
from __future__ import annotations

from typing import Any

from .proof import build_proof
from .verify import verify_claim


def verify_and_prove(store: Any, claim_id: str) -> dict[str, Any]:
    """Re-verify a claim, then return its current verdict and proof bundle."""
    claim = store.get_claim(claim_id)
    if claim is None:
        raise KeyError(f"Unknown claim: {claim_id}")
    claim = verify_claim(store, claim)
    proof = build_proof(store, claim.id)
    return {
        "claim_id": claim.id,
        "verdict": claim.status,
        "verified_at": claim.verified_at.isoformat() if claim.verified_at else None,
        "proof": proof,
    }


def proof_status(store: Any, claim_id: str) -> dict[str, Any]:
    """Return proof without changing the stored claim decision."""
    proof = build_proof(store, claim_id)
    return {
        "claim_id": claim_id,
        "verdict": proof["claim"]["status"],
        "ledger_integrity": proof["ledger"]["integrity"],
        "content_sha256": proof["content_sha256"],
        "proof": proof,
    }
