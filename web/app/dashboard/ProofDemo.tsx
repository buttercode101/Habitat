"use client";

import { useState } from "react";

const ORIGINAL = {
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

function canonical(value: any): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  return JSON.stringify(value);
}

async function digest(proof: any) {
  const copy = JSON.parse(JSON.stringify(proof));
  delete copy.generated_at;
  delete copy.content_sha256;
  const bytes = new TextEncoder().encode(canonical(copy));
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

export default function ProofDemo() {
  const [proof, setProof] = useState(ORIGINAL);
  const [verified, setVerified] = useState<boolean | null>(null);
  const tampered = proof.claim.evidence.details.summary !== ORIGINAL.claim.evidence.details.summary;
  const stateLabel = tampered ? "TAMPERED" : verified === true ? "VERIFIED" : "READY";

  async function verify() {
    setVerified((await digest(proof)) === proof.content_sha256);
  }

  function tamper() {
    setProof((current) => ({...current, claim: {...current.claim, evidence: {...current.claim.evidence, details: {...current.claim.evidence.details, summary: "Changed after the proof was generated."}}}}));
    setVerified(null);
  }

  function reset() { setProof(ORIGINAL); setVerified(null); }

  function download() {
    const blob = new Blob([JSON.stringify(proof, null, 2) + "\n"], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "habitat-proof-rosendaltown.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section id="proof-demo" className="proof-demo-section">
      <div className="section-head"><div><p className="eyebrow">Proof inspector</p><h2>Break the proof on purpose.</h2></div><span className="muted">Browser verification · no backend required</span></div>
      <div className="proof-demo-banner">
        <div><span className={`status ${tampered ? "attention" : verified === true ? "ok" : ""}`}>{stateLabel}</span><strong>{verified === true ? "Digest matches." : verified === false ? "Digest mismatch detected." : "Ready to verify."}</strong></div>
        <div className="actions">
          <button className="button primary" onClick={verify}>Verify proof</button>
          <button className="button" onClick={tamper}>Simulate tampering</button>
          <button className="button" onClick={reset}>Reset</button>
          <button className="button" onClick={download}>Download JSON</button>
        </div>
      </div>
      <div className="proof-grid">
        <article className="proof-card"><h2>Claim</h2><div className="claim-statement">{proof.claim.claim}</div><Row label="Action" value={proof.claim.action}/><Row label="Run ID" value={proof.claim.run_id}/><Row label="Expected" value={proof.claim.expected_status}/></article>
        <article className="proof-card"><h2>Evidence</h2><Row label="Source" value={proof.claim.evidence.source}/><Row label="Action ID" value={proof.claim.evidence.action_id}/><Row label="Repository" value={proof.claim.evidence.details.repo}/><Row label="Commit" value={proof.claim.evidence.details.commit}/><Row label="Ledger" value={proof.ledger.integrity}/></article>
      </div>
      <article className="proof-card action-detail"><div className="proof-card-head"><div><p className="eyebrow">Integrity</p><h2>Content digest</h2></div><span className="mono">{proof.content_sha256}</span></div><p className="proof-explain">Habitat hashes the canonical proof contents, excluding the generated timestamp and the digest itself. Change one field and the digest no longer matches.</p><div className="digest-state"><span className={verified === false ? "bad" : verified === true ? "good" : "neutral"}>{verified === false ? "✕ DIGEST MISMATCH" : verified === true ? "✓ DIGEST VERIFIED" : "○ READY TO VERIFY"}</span><code>{proof.content_sha256}</code></div></article>
    </section>
  );
}

function Row({label,value}:{label:string;value:string|null|undefined}) {
  return <div className="row"><span>{label}</span><b>{value || "—"}</b></div>;
}
