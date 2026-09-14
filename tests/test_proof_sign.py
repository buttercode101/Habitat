import pytest

from habitat.proof_sign import generate_keypair, sign_proof, verify_signed_proof


def test_signed_proof_round_trip():
    pytest.importorskip("cryptography")
    private, _ = generate_keypair()
    bundle = {"proof_version": "1", "content_sha256": "abc", "claim": {"id": "c1", "status": "verified"}}
    signed = sign_proof(bundle, private, "test-key")
    assert signed["signature"]["algorithm"] == "Ed25519"
    assert signed["signature"]["key_id"] == "test-key"
    assert verify_signed_proof(signed)


def test_signed_proof_tamper_is_rejected():
    pytest.importorskip("cryptography")
    private, _ = generate_keypair()
    signed = sign_proof({"proof_version": "1", "content_sha256": "abc"}, private)
    signed["content_sha256"] = "changed"
    assert not verify_signed_proof(signed)
