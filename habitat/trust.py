"""Small trust registry for signed proof verification.

The registry is deliberately explicit: a valid Ed25519 signature is not treated
as trusted until its key ID and public key are present in the caller's registry.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .proof_sign import verify_signed_proof


@dataclass(frozen=True)
class TrustedKey:
    key_id: str
    public_key: str
    agent_id: str | None = None
    expires_at: datetime | None = None
    enabled: bool = True


class TrustRegistry:
    def __init__(self, keys: Iterable[TrustedKey] = ()):
        self._keys = {key.key_id: key for key in keys}

    def add(self, key: TrustedKey) -> None:
        self._keys[key.key_id] = key

    def revoke(self, key_id: str) -> None:
        key = self._keys.get(key_id)
        if key:
            self._keys[key_id] = TrustedKey(key.key_id, key.public_key, key.agent_id, key.expires_at, False)

    def get(self, key_id: str) -> TrustedKey | None:
        return self._keys.get(key_id)

    def is_trusted(self, key_id: str, public_key: str, now: datetime | None = None) -> bool:
        key = self._keys.get(key_id)
        if not key or not key.enabled or key.public_key != public_key:
            return False
        current = now or datetime.now().astimezone()
        return key.expires_at is None or current < key.expires_at

    def verify(self, bundle: dict, now: datetime | None = None) -> bool:
        signature = bundle.get("signature")
        if not isinstance(signature, dict):
            return False
        key_id = signature.get("key_id")
        public_key = signature.get("public_key")
        return bool(key_id and public_key and self.is_trusted(key_id, public_key, now) and verify_signed_proof(bundle))
