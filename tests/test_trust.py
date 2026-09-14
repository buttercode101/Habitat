import pytest
from datetime import datetime, timezone, timedelta

from habitat.proof_sign import generate_keypair, sign_proof
from habitat.trust import TrustRegistry, TrustedKey

pytest.importorskip("cryptography")


def test_registry_requires_explicit_key_trust():
    private, public = generate_keypair()
    bundle = sign_proof({"proof_version": "1", "content_sha256": "abc"}, private, "agent-key")
    registry = TrustRegistry([TrustedKey("agent-key", public)])
    assert registry.verify(bundle)


def test_registry_rejects_revoked_or_expired_key():
    private, public = generate_keypair()
    bundle = sign_proof({"proof_version": "1"}, private, "agent-key")
    registry = TrustRegistry([TrustedKey("agent-key", public, expires_at=datetime.now(timezone.utc) - timedelta(seconds=1))])
    assert not registry.verify(bundle)
    registry.add(TrustedKey("agent-key", public))
    assert registry.verify(bundle)
    registry.revoke("agent-key")
    assert not registry.verify(bundle)
