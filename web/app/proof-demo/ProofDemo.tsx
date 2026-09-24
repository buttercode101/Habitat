"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

type Proof = {
  proof_version: string;
  generated_at: string;
  content_sha256: string;
  claim: {
    id: string;
    habitat_id: string;
    job_id: string | null;
    claim: string;
    action: string;
    expected_status: string;
    created_at: string;
    verified_at: string;
    status: string;
    evidence: {
      action: string;
      action_id: string;
      details: Record<string, string>;
      run_id: string;
      source: string;
      status: string;
      timestamp: string;
    };
    run_id: string;
  };
  ledger: {
    integrity: string;
    actions: Array<{
      id: string;
      habitat_id: string;
      job_id: string | null;
      timestamp: string;
      actor: string;
      action: string;
      status: string;
      details: Record<string, string>;
      run_id: string;
    }>;
  };
};

const ORIGINAL: Proof = {
  proof_version: "1",
  generated_at: "2026-09-15T13:39:37.600511+00:00",
  content_sha256: "a21b7f2ff7c25c6b87d6d502bb0916d7423f4f46f3bb1f8349ddcf00818fc088",
  claim: {
    id: "7b0dfe4e-fa51-44a7-8549-428083b666d9",
    habitat_id: "real-projects",
    job_id: null,
    claim: "Shipped Rosendaltown change: corrected category image/content mapping and refreshed homepage imagery with the real Rosendal photos.",
    action: "commit",
    expected_status: "ok",
    created_at: "2026-09-15T13:39:37.597558+00:00",
    verified_at: "2026-09-15T13:39:37.599886+00:00",
    status: "verified",
    evidence: {
      action: "commit",
      action_id: "rosendaltown-commit-45bc7aa7f945",
      details: {
        commit: "45bc7aa7f9458ced34c97cd76a7e833c71632aaa",
        repo: "buttercode101/rosendaltown",
        source: "existing_real_project_commit",
        summary: "Fix category image/content mismatch by mapping real Rosendal photos to each listing and updating homepage/category imagery.",
        url: "https://github.com/buttercode101/rosendaltown/commit/45bc7aa7f9458ced34c97cd76a7e833c71632aaa"
      },
      run_id: "45bc7aa7f9458ced34c97cd76a7e833c71632aaa",
      source: "habitat_trusted_ledger",
      status: "ok",
      timestamp: "2026-09-15T13:39:37.000666+00:00"
    },
    run_id: "45bc7aa7f9458ced34c97cd76a7e833c71632aaa"
  },
  ledger: {
    integrity: "intact",
    actions: [{
      action: "commit",
      actor: "github",
      details: {
        commit: "45bc7aa7f9458ced34c97cd76a7e833c71632aaa",
        repo: "buttercode101/rosendaltown",
        source: "existing_real_project_commit",
        summary: "Fix category image/content mismatch by mapping real Rosendal photos to each listing and updating homepage/category imagery.",
        url: "https://github.com/buttercode101/rosendaltown/commit/45bc7aa7f9458ced34c97cd76a7e833c71632aaa"
      },
      habitat_id: "real-projects",
      id: "rosendaltown-commit-45bc7aa7f945",
      job_id: null,
      run_id: "45bc7aa7f9458ced34c97cd76a7e833c71632aaa",
      status: "ok",
      timestamp: "2026-09-15T13:39:37.000666+00:00"
    }]
  }
};

function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value as Record<string, unknown>).sort().map((key) => `${JSON.stringify(key)}:${canonical((value as Record<string, unknown>)[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function digestInput(proof: Proof) {
  const copy = JSON.parse(JSON.stringify(proof)) as Record<string, unknown>;
  delete copy.generated_at;
  delete copy.content_sha256;
  return copy;
}

async function sha256(value: string) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

export default function ProofDemo() {
  const [proof, setProof] = useState(ORIGINAL);
  const [verified, setVerified] = useState<boolean | null>(null);
  const [busy, setBusy] = useState(false);

  const tampered = proof.claim.evidence.details.summary !== ORIGINAL.claim.evidence.details.summary;
  const status = useMemo(() => tampered ? "TAMPERED" : "VERIFIED", [tampered]);

  async function verify() {
    setBusy(true);
    const digest = await sha256(canonical(digestInput(proof)));
    setVerified(digest === proof.content_sha256);
    setBusy(false);
  }

  function simulateTamper() {
    setProof((current) => ({
      ...current,
      claim: {
        ...current.claim,
        evidence: {
          ...current.claim.evidence,
          details: {
            ...current.claim.evidence.details,
            summary: "Changed after the proof was generated."
          }
        }
      }
    }));
    setVerified(null);
  }

  function reset() {
    setProof(ORIGINAL);
    setVerified(null);
  }

  function download() {
    const blob = new Blob([JSON.stringify(proof, null, 2) + "\n"], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "habitat-proof-rosendaltown.json";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <>
      <section className="inspector-head">
        <Link className="back" href="/">← Habitat home</Link>
        <p className="eyebrow">A real checked-in proof</p>
        <h1>Inspect the evidence. Then try to break it.</h1>
        <p className="lede">This is the actual Rosendaltown proof artifact committed to Habitat. The browser verifier reproduces Habitat&apos;s canonical SHA-256 content check without needing a backend.</p>
      </section>

      <section className="proof-demo-banner">
        <div>
          <span className={`status ${status === "VERIFIED" ? "ok" : "attention"}`}>{status}</span>
          <strong>{verified === true ? "Digest matches the proof." : verified === false ? "Digest mismatch detected." : "Ready to verify."}</strong>
        </div>
        <div className="actions">
          <button className="button primary" onClick={verify} disabled={busy}>{busy ? "Verifying…" : "Verify proof"}</button>
          <button className="button" onClick={simulateTamper}>Simulate tampering</button>
          <button className="button" onClick={reset}>Reset</button>
          <button className="button" onClick={download}>Download JSON</button>
        </div>
      </section>

      <section className="proof-grid">
        <article className="proof-card">
          <h2>Claim</h2>
          <div className="claim-statement">{proof.claim.claim}</div>
          <Row label="Action" value={proof.claim.action} />
          <Row label="Run ID" value={proof.claim.run_id} />
          <Row label="Expected" value={proof.claim.expected_status} />
          <Row label="Habitat status" value={proof.claim.status} />
        </article>
        <article className="proof-card">
          <h2>Evidence</h2>
          <Row label="Source" value={proof.claim.evidence.source} />
          <Row label="Action ID" value={proof.claim.evidence.action_id} />
          <Row label="Repository" value={proof.claim.evidence.details.repo} />
          <Row label="Commit" value={proof.claim.evidence.details.commit} />
          <Row label="Ledger" value={proof.ledger.integrity} />
        </article>
      </section>

      <section className="proof-card action-detail">
        <div className="proof-card-head"><div><p className="eyebrow">Integrity</p><h2>Content digest</h2></div><span className="mono">{proof.content_sha256}</span></div>
        <p className="proof-explain">Habitat hashes the canonical proof contents, excluding the generated timestamp and the digest itself. Change one field and the digest no longer matches.</p>
        <div className="digest-state"><span className={verified === false ? "bad" : "good"}>{verified === false ? "✕ DIGEST MISMATCH" : "✓ SHA-256 CONTENT DIGEST"}</span><code>{proof.content_sha256}</code></div>
      </section>

      <section className="notice">
        <strong>Interpretation boundary</strong>
        <span>A valid proof establishes the integrity and consistency of the supplied evidence. It does not by itself establish publisher trust or real-world truth.</span>
      </section>

      <section className="proof-demo-footer">
        <Link className="button" href="/dashboard">Open dashboard</Link>
        <a className="button" href="https://github.com/buttercode101/Habitat/blob/main/proofs/rosendaltown-45bc7aa7.json">View source proof ↗</a>
      </section>
    </>
  );
}

function Row({ label, value }: { label: string; value: string | null | undefined }) {
  return <div className="row"><span>{label}</span><b>{value || "—"}</b></div>;
}
