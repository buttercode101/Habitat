import Link from "next/link";
import type { Metadata } from "next";
import { getClaims, getStatus, type Claim } from "../../lib/habitat";

export const metadata: Metadata = {
  title: "Habitat Dashboard",
  robots: { index: false, follow: false },
};

function errorMessage(error: unknown) {
  return error instanceof Error ? error.message : "Unable to reach the Habitat backend";
}

export default async function DashboardPage() {
  try {
    const [status, claims] = await Promise.all([getStatus(), getClaims()]);
    const attention = claims.filter((claim) => claim.status !== "verified").length;
    return <Dashboard status={status} claims={claims} attention={attention} />;
  } catch (error) {
    return (
      <main className="shell">
        <header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">CONTROL PLANE UI</span></header>
        <section className="hero compact"><Link className="back" href="/">← Back to Habitat</Link><p className="eyebrow">Backend connection required</p><h1>The inspection surface is ready. The Habitat service is not connected.</h1><p className="lede">{errorMessage(error)}</p><div className="notice"><strong>Configure the deployment</strong><span>Set <code>HABITAT_API_URL</code> to the persistent Habitat service and <code>HABITAT_API_TOKEN</code> to its server bearer secret.</span></div></section>
      </main>
    );
  }
}

function Dashboard({ status, claims, attention }: { status: Awaited<ReturnType<typeof getStatus>>; claims: Claim[]; attention: number }) {
  return (
    <main className="shell">
      <header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">ACCOUNTABILITY SURFACE</span></header>
      <section className="hero compact"><Link className="back" href="/">← Habitat home</Link><p className="eyebrow">{status.name}</p><h1>Inspect what your agents actually did.</h1><p className="lede">A live inspection surface over Habitat's persistent ledger, policy checks, claims and portable proofs.</p><div className="flow"><span>Agent</span><i>→</i><span>Event</span><i>→</i><span>Ledger</span><i>→</i><span>Verify</span><i>→</i><span>Proof</span></div></section>
      <section className="metrics" aria-label="Habitat status"><Metric label="Jobs" value={status.jobs} /><Metric label="Agents" value={status.agents} /><Metric label="Active signals" value={status.active_signals} /><Metric label="Needs attention" value={attention} /></section>
      <section className="section-head"><div><p className="eyebrow">Claims</p><h2>Evidence worth inspecting</h2></div><span className="muted">Live from Habitat</span></section>
      {claims.length === 0 ? <div className="empty">No claims recorded yet. Habitat will surface them here when agents produce policy-checked evidence.</div> : <div className="claims">{claims.map((claim) => <ClaimCard key={claim.id} claim={claim} />)}</div>}
      <footer><Link href="/">Habitat</Link> · Vercel is the presentation layer. Habitat remains the source of truth.</footer>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>;
}

function ClaimCard({ claim }: { claim: Claim }) {
  const verified = claim.status === "verified";
  return <article className="claim-card"><div className="claim-top"><span className={`status ${verified ? "ok" : "attention"}`}>{claim.status || "unknown"}</span><span className="mono">{claim.id}</span></div><h3>{claim.statement || "Claim without a statement"}</h3><div className="meta"><span>Agent <b>{claim.agent_id || "—"}</b></span><span>Run <b>{claim.run_id || "—"}</b></span><span>Expected <b>{claim.expected_status || "—"}</b></span></div><div className="actions"><Link className="button primary" href={`/claims/${encodeURIComponent(claim.id)}`}>Inspect claim</Link><a className="button" href={`/api/claims/${encodeURIComponent(claim.id)}/verify`}>Verify now</a></div></article>;
}
