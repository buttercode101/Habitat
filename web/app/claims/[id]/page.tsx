import Link from "next/link";
import { getProof } from "../../../lib/habitat";

type JsonObject = Record<string, unknown>;

function object(value: unknown): JsonObject {
  return value && typeof value === "object" && !Array.isArray(value) ? value as JsonObject : {};
}

function field(value: unknown) {
  return value === undefined || value === null || value === "" ? "—" : String(value);
}

function actionFor(proof: JsonObject, actionId: unknown) {
  const actions = Array.isArray(object(proof.ledger).actions) ? object(proof.ledger).actions : [];
  return actions.map(object).find((action) => action.id === actionId) || null;
}

export default async function ClaimPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  try {
    const result = object(await getProof(id));
    const proof = object(result.proof);
    const claim = object(proof.claim);
    const evidence = object(claim.evidence);
    const action = actionFor(proof, evidence.action_id);
    const signature = object(proof.signature);
    const hasSignature = Object.keys(signature).length > 0;
    const ledger = object(proof.ledger);

    return (
      <main className="shell">
        <header className="topbar">
          <Link className="brand" href="/">Habitat</Link>
          <span className="pill">PROOF INSPECTOR</span>
        </header>
        <section className="inspector-head">
          <Link className="back" href="/">← All claims</Link>
          <p className="eyebrow">Claim</p>
          <h1>{field(claim.claim)}</h1>
          <span className="mono">{id}</span>
        </section>
        <section className="proof-grid">
          <Card title="Verification">
            <Row label="Verdict" value={result.verdict ?? claim.status} />
            <Row label="Expected" value={claim.expected_status} />
            <Row label="Evidence source" value={evidence.source} />
            <Row label="Action ID" value={evidence.action_id} />
            <Row label="Run ID" value={claim.run_id} />
            <Row label="Job ID" value={claim.job_id} />
            <Row label="Verified at" value={claim.verified_at} />
          </Card>
          <Card title="Proof integrity">
            <Row label="Ledger integrity" value={result.ledger_integrity ?? ledger.integrity} />
            <Row label="Content SHA-256" value={result.content_sha256 ?? proof.content_sha256} />
            <Row label="Signature" value={hasSignature ? "present" : "not present"} />
            {hasSignature && <Row label="Signature algorithm" value={signature.algorithm} />}
          </Card>
        </section>
        {action && (
          <section className="proof-card action-detail">
            <h2>Correlated action</h2>
            <div className="proof-grid compact-grid">
              <Row label="Action" value={action.action} />
              <Row label="Status" value={action.status} />
              <Row label="Timestamp" value={action.timestamp} />
              <Row label="Actor" value={action.actor} />
            </div>
          </section>
        )}
        <section className="notice">
          <strong>Interpretation boundary</strong>
          <span>A valid proof establishes the integrity and consistency of the supplied evidence. It does not by itself establish publisher trust or real-world truth.</span>
        </section>
        <div className="actions">
          <a className="button primary" href={`/api/claims/${encodeURIComponent(id)}/verify`}>Verify now</a>
          <a className="button" href={`/api/claims/${encodeURIComponent(id)}/proof`}>Proof JSON</a>
        </div>
      </main>
    );
  } catch (error) {
    return (
      <main className="shell">
        <header className="topbar"><Link className="brand" href="/">Habitat</Link><span className="pill">PROOF INSPECTOR</span></header>
        <section className="hero compact">
          <p className="eyebrow">Claim unavailable</p>
          <h1>Habitat could not load this proof.</h1>
          <p className="lede">{error instanceof Error ? error.message : "Unknown backend error"}</p>
          <Link className="button primary" href="/">Back to dashboard</Link>
        </section>
      </main>
    );
  }
}

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return <article className="proof-card"><h2>{title}</h2>{children}</article>;
}

function Row({ label, value }: { label: string; value: unknown }) {
  return <div className="row"><span>{label}</span><b>{field(value)}</b></div>;
}
