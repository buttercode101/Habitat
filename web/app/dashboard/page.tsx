import Link from "next/link";
import type { Metadata } from "next";
import { getClaims, getStatus, type Claim } from "../../lib/habitat";
import ProofDemo from "./ProofDemo";

export const metadata: Metadata = {
  title: "Habitat Dashboard",
  robots: { index: false, follow: false },
};

function errorMessage(error: unknown) {
  return error instanceof Error ? error.message : "Unable to reach the Habitat backend";
}

const DEMO_CLAIM: Claim = {
  id: "7b0dfe4e-fa51-44a7-8549-428083b666d9",
  agent_id: "github",
  run_id: "45bc7aa7f9458ced34c97cd76a7e833c71632aaa",
  statement: "Shipped Rosendaltown change: corrected category image/content mapping and refreshed homepage imagery with the real Rosendal photos.",
  expected_status: "ok",
  status: "verified",
};

export default async function DashboardPage() {
  try {
    const [status, claims] = await Promise.all([getStatus(), getClaims()]);
    const attention = claims.filter((claim) => claim.status !== "verified").length;
    return <Dashboard status={status} claims={claims} attention={attention} live />;
  } catch (error) {
    return <DemoDashboard error={errorMessage(error)} />;
  }
}

function DemoDashboard({ error }: { error: string }) {
  return (
    <main className="shell">
      <header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">DEMO MODE</span></header>
      <section className="hero compact">
        <Link className="back" href="/">← Back to Habitat</Link>
        <p className="eyebrow">Interactive proof surface</p>
        <h1>See Habitat working without connecting a backend.</h1>
        <p className="lede">The hosted dashboard is presentation-only until a Habitat service is configured. Instead of leaving you at an error screen, this deployment now ships with a real repository proof you can inspect and verify in-browser.</p>
        <div className="notice"><strong>Live backend unavailable</strong><span>{error}. Showing the checked-in Rosendaltown proof as an explicit demo — no fake live data.</span></div>
      </section>
      <section className="metrics" aria-label="Demo proof status">
        <Metric label="Claims" value={1} />
        <Metric label="Verified" value={1} />
        <Metric label="Ledger" value={1} />
        <Metric label="Mode" value="DEMO" />
      </section>
      <section className="section-head"><div><p className="eyebrow">Repository proof</p><h2>One real claim, ready to inspect</h2></div><span className="muted">Checked-in artifact</span></section>
      <div className="claims"><ClaimCard claim={DEMO_CLAIM} demo /></div>
      <ProofDemo />
      <footer><Link href="/">Habitat</Link> · Demo mode is explicit. A configured Habitat service becomes the source of truth.</footer>
    </main>
  );
}

function Dashboard({ status, claims, attention, live }: { status: Awaited<ReturnType<typeof getStatus>>; claims: Claim[]; attention: number; live: boolean }) {
  return (
    <main className="shell">
      <header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">{live ? "LIVE ACCOUNTABILITY SURFACE" : "ACCOUNTABILITY SURFACE"}</span></header>
      <section className="hero compact"><Link className="back" href="/">← Habitat home</Link><p className="eyebrow">{status.name}</p><h1>Inspect what your agents actually did.</h1><p className="lede">A live inspection surface over Habitat's persistent ledger, policy checks, claims and portable proofs.</p><div className="flow"><span>Agent</span><i>→</i><span>Event</span><i>→</i><span>Ledger</span><i>→</i><span>Verify</span><i>→</i><span>Proof</span></div></section>
      <section className="metrics" aria-label="Habitat status"><Metric label="Jobs" value={status.jobs} /><Metric label="Agents" value={status.agents} /><Metric label="Active signals" value={status.active_signals} /><Metric label="Needs attention" value={attention} /></section>
      <section className="section-head"><div><p className="eyebrow">Claims</p><h2>Evidence worth inspecting</h2></div><span className="muted">Live from Habitat</span></section>
      {claims.length === 0 ? <div className="empty">No claims recorded yet. Habitat will surface them here when agents produce policy-checked evidence.</div> : <div className="claims">{claims.map((claim) => <ClaimCard key={claim.id} claim={claim} />)}</div>}
      <footer><Link href="/">Habitat</Link> · Vercel is the presentation layer. Habitat remains the source of truth.</footer>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>;
}

function ClaimCard({ claim, demo = false }: { claim: Claim; demo?: boolean }) {
  const verified = claim.status === "verified";
  return <article className="claim-card"><div className="claim-top"><span className={`status ${verified ? "ok" : "attention"}`}>{claim.status || "unknown"}</span><span className="mono">{claim.id}</span></div><h3>{claim.statement || "Claim without a statement"}</h3><div className="meta"><span>Agent <b>{claim.agent_id || "—"}</b></span><span>Run <b>{claim.run_id || "—"}</b></span><span>Expected <b>{claim.expected_status || "—"}</b></span></div><div className="actions">{demo ? <Link className="button primary" href="/dashboard#proof-demo">Inspect proof</Link> : <><Link className="button primary" href={`/claims/${encodeURIComponent(claim.id)}`}>Inspect claim</Link><a className="button" href={`/api/claims/${encodeURIComponent(claim.id)}/verify`}>Verify now</a></>}</div></article>;
}
