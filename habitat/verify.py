"""Deterministic claim verification with exact run correlation and policy gates."""
from __future__ import annotations
from typing import Any
from .claims import Claim
from .store import Store
from .schema import utcnow
from .adapters import EvidenceAdapter
from .policy import EvidencePolicy, apply_policy


def _matches_expected(data: Any, expected: dict[str, Any] | None) -> bool:
    if not expected:
        return True
    return isinstance(data, dict) and all(data.get(k) == v for k, v in expected.items())


def _finish(claim: Claim, store: Store, policy: EvidencePolicy | None = None) -> Claim:
    if policy and claim.status == "verified":
        decision = apply_policy(policy, claim.evidence)
        claim.evidence = {**claim.evidence, "policy": decision}
        if decision["status"] != "allowed":
            claim.status = "rejected"
    claim.verified_at = utcnow()
    store.save_claim(claim)
    return claim


def verify_claim(
    store: Store,
    claim: Claim,
    evidence_adapter: EvidenceAdapter | None = None,
    evidence_query: str | None = None,
    evidence_expected: dict[str, Any] | None = None,
    policy: EvidencePolicy | None = None,
) -> Claim:
    """Verify a claim, then apply an optional policy as a final non-positive gate.

    Policies can only downgrade a verified result; they can never turn missing or
    rejected evidence into a positive verification.
    """
    if claim.habitat_id != store.habitat().id:
        claim.status = "rejected"
        claim.evidence = {"source": "habitat", "reason": "habitat_mismatch"}
        return _finish(claim, store, policy)
    if not store.verify_action_integrity():
        claim.status = "inconclusive"
        claim.evidence = {"source": "habitat_trusted_ledger", "reason": "action_ledger_integrity_check_failed"}
        return _finish(claim, store, policy)

    actions = store.actions(5000)
    matches = [a for a in actions if (claim.job_id is None or a.job_id == claim.job_id) and (claim.action is None or a.action == claim.action) and (claim.run_id is None or a.run_id == claim.run_id)]

    if claim.run_id is None and (claim.job_id or claim.action):
        if len(matches) == 1:
            trusted = matches[0] if matches[0].status == claim.expected_status else None
            if trusted:
                claim.status = "verified"
                claim.evidence = {"source": "habitat_trusted_ledger", "action_id": trusted.id, "action": trusted.action, "status": trusted.status, "timestamp": trusted.timestamp.isoformat(), "run_id": trusted.run_id, "legacy_match": True, "details": trusted.details}
            else:
                claim.status = "rejected"
                claim.evidence = {"source": "habitat_trusted_ledger", "reason": "matching_action_has_different_status", "legacy_match": True}
            return _finish(claim, store, policy)
        matches = []
        if not evidence_adapter:
            claim.status = "rejected" if len(actions) == 0 else "inconclusive"
            claim.evidence = {"source": "habitat_trusted_ledger", "reason": "no_matching_trusted_action" if not actions else "run_id_required_for_ambiguous_trusted_verification"}
            return _finish(claim, store, policy)

    trusted = next((a for a in matches if a.status == claim.expected_status), None)
    if trusted:
        claim.status = "verified"
        claim.evidence = {"source": "habitat_trusted_ledger", "action_id": trusted.id, "action": trusted.action, "status": trusted.status, "timestamp": trusted.timestamp.isoformat(), "run_id": trusted.run_id, "details": trusted.details}
    elif matches:
        claim.status = "rejected"
        claim.evidence = {"source": "habitat_trusted_ledger", "reason": "matching_action_has_different_status", "observed": [{"action": a.action, "status": a.status, "run_id": a.run_id} for a in matches[:5]]}
    elif evidence_adapter and evidence_query:
        evidence = evidence_adapter.observe(evidence_query)
        if evidence.observed and evidence.status == claim.expected_status and _matches_expected(evidence.data, evidence_expected):
            claim.status = "verified"
            claim.evidence = {"source": evidence.source, "status": evidence.status, "data": evidence.data, "query": evidence_query, "expected": evidence_expected or {}}
        elif evidence.error:
            claim.status = "inconclusive"
            claim.evidence = {"source": evidence.source, "reason": evidence.error, "query": evidence_query}
        else:
            claim.status = "rejected"
            claim.evidence = {"source": evidence.source, "reason": "external_evidence_did_not_match", "status": evidence.status, "data": evidence.data, "query": evidence_query, "expected": evidence_expected or {}}
    else:
        claim.status = "rejected"
        claim.evidence = {"source": "habitat_trusted_ledger", "reason": "no_matching_trusted_action"}
    return _finish(claim, store, policy)
