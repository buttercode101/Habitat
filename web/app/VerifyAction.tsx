"use client";

import { useState } from "react";

type Result = {
  verdict: string;
  ledger: string;
  digest: string;
};

export default function VerifyAction({ endpoint }: { endpoint: string }) {
  const [pending, setPending] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");

  async function verify() {
    if (pending) return;
    setPending(true);
    setError("");
    setResult(null);
    try {
      const response = await fetch(endpoint, {
        method: "GET",
        cache: "no-store",
        headers: { Accept: "application/json" },
      });
      const payload: unknown = await response.json();
      if (!response.ok || !payload || typeof payload !== "object") {
        throw new Error("Habitat could not complete this verification.");
      }
      const data = payload as Record<string, unknown>;
      if (typeof data.error === "string") {
        throw new Error("Habitat could not complete this verification.");
      }
      const proof = data.proof && typeof data.proof === "object"
        ? data.proof as Record<string, unknown>
        : {};
      const claim = proof.claim && typeof proof.claim === "object"
        ? proof.claim as Record<string, unknown>
        : {};
      const ledgerData = proof.ledger && typeof proof.ledger === "object"
        ? proof.ledger as Record<string, unknown>
        : {};
      const verdict = data.verdict ?? claim.status;
      if (typeof verdict !== "string" || !verdict.trim()) {
        throw new Error("The verifier returned no verdict. No success is assumed.");
      }
      setResult({
        verdict,
        ledger: String(data.ledger_integrity ?? ledgerData.integrity ?? "not reported"),
        digest: String(data.content_sha256 ?? proof.content_sha256 ?? "not reported"),
      });
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Verification failed. Try again.");
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="verify-action">
      <button className="button primary" type="button" onClick={verify} disabled={pending}>
        {pending ? <><span className="verify-spinner" aria-hidden="true" /> Verifying…</> : "Verify now"}
      </button>
      {error && <p className="verify-feedback is-error" role="alert">{error}</p>}
      {result && (
        <div className="verify-feedback" role="status" aria-live="polite">
          <strong>Verifier response: {result.verdict}</strong>
          <span>Ledger integrity: {result.ledger}</span>
          <span className="verify-digest">SHA-256: {result.digest}</span>
          <small>A verifier response describes the supplied evidence; it does not establish publisher trust or external-world truth.</small>
        </div>
      )}
    </div>
  );
}
