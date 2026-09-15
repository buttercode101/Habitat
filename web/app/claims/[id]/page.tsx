import Link from "next/link";
import { getProof } from "../../../lib/habitat";

function field(value: unknown) {
  return value === undefined || value === null || value === "" ? "—" : String(value);
}

export default async function ClaimPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  try {
    const proof = await getProof(id);
    const claim = (proof.claim || {}) as Record<string, unknown>;
    const evidence = (claim.evidence || proof.evidence || {}) as Record<string, unknown>;
    const assurance = (proof.assurance || {}) as Record<string, unknown>;
    return <main className="shell"><header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">PROOF INSPECTOR</span></header><section className="inspector-head"><Link className="back" href="/">← All claims</Link><p className="eyebrow">Claim</p><h1>{field(claim.statement)}</h1><span className="mono">{id}</span></section><section className="proof-grid"><Card title="Verification"><Row label="Status" value={claim.status} /><Row label="Expected" value={claim.expected_status} /><Row label="Evidence source" value={evidence.source} /><Row label="Action ID" value={evidence.action_id} /><Row label="Run ID" value={claim.run_id} /><Row label="Job ID" value={claim.job_id} /></Card><Card title="Assurance"><Row label="Structural validity" value={assurance.structural_validity} /><Row label="Content integrity" value={assurance.content_integrity} /><Row label="Internal consistency" value={assurance.internal_consistency} /><Row label="Signature" value={assurance.signature || (proof.signature ? "present" : "not present")} /><Row label="Publisher trust" value={assurance.publisher_trust || "not established"} /><Row label="External truth" value={assurance.external_truth || "not established"} /></Card></section><section className="notice"><strong>Interpretation boundary</strong><span>A valid proof establishes the integrity and consistency of the supplied evidence. It does not by itself establish publisher trust or real-world truth.</span></section><div className="actions"><a className="button primary" href={`/api/claims/${encodeURIComponent(id)}/verify`}>Verify now</a><a className="button" href={`/api/claims/${encodeURIComponent(id)}/proof`}>Proof JSON</a></div></main>;
  } catch (error) {
    return <main className="shell"><header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">PROOF INSPECTOR</span></header><section className="hero compact"><p className="eyebrow">Claim unavailable</p><h1>Habitat could not load this proof.</h1><p className="lede">{error instanceof Error ? error.message : "Unknown backend error"}</p><Link className="button primary" href="/">Back to dashboard</Link></section></main>;
  }
}

function Card({ title, children }: { title: string; children: React.ReactNode }) { return <article className="proof-card"><h2>{title}</h2>{children}</article>; }
function Row({ label, value }: { label: string; value: unknown }) { return <div className="row"><span>{label}</span><b>{field(value)}</b></div>; }
