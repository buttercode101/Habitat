import Link from "next/link";
import manifest from "../../public/proofs-manifest.json";

export const metadata = {
  title: "Evidence — Habitat",
  description: "A reconciled set of checked-in proof artifacts.",
};

const proofs = Object.entries(manifest.projects).flatMap(([project, runs]) =>
  runs.map((proof) => ({ ...proof, project }))
);

export default function EvidencePage() {
  return (
    <>
      <nav className="topbar" role="navigation" aria-label="Main">
        <Link className="brand" href="/" aria-label="Habitat home">Habitat</Link>
        <div className="nav-links">
          <Link href="/" className="pill">Home</Link>
          <Link href="/evidence" className="pill" aria-current="page">Evidence</Link>
          <Link href="/dashboard" className="pill">Dashboard</Link>
          <a href="https://github.com/buttercode101/Habitat" target="_blank" rel="noopener noreferrer" className="pill">GitHub</a>
        </div>
      </nav>

      <main id="main-content" tabIndex={-1} className="shell">
        <header className="hero compact">
          <p className="eyebrow">Reconciled proof archive</p>
          <h1>Proofs we can actually stand behind.</h1>
          <p className="lede">
            This surface intentionally shows only proof artifacts whose checked-in path,
            run ID and claim were reconciled against the artifact itself. Historical proof
            paths remain excluded until their provenance is repaired.
          </p>
          <div className="flow">
            <Link href="/verify-all.sh" download className="button primary">Download verify-all.sh</Link>
            <span>or</span>
            <Link href="/proofs-manifest.json" target="_blank" className="button secondary">Browse manifest</Link>
          </div>
        </header>

        <section aria-labelledby="projects-heading">
          <h2 id="projects-heading" className="section-title">Reconciled proof artifacts</h2>
          <div className="projects-grid">
            {proofs.map((proof) => (
              <article key={proof.run_id} className="project-card">
                <h3 className="project-name">{proof.project}</h3>
                <Link href={new URL(proof.proof_url).pathname} className="proof-card" target="_blank" rel="noopener noreferrer">
                  <div className="proof-top">
                    <span className="proof-id">{proof.run_id}</span>
                    <span className="status ok"><span className="dot" aria-hidden="true" />RECONCILED</span>
                  </div>
                  <p className="proof-commit">{proof.claim}</p>
                  <div className="proof-digest"><span>Digest</span><b className="mono">{proof.content_sha256.slice(0, 8)}…{proof.content_sha256.slice(-4)}</b></div>
                </Link>
              </article>
            ))}
          </div>
        </section>

        <section className="stress-section" aria-labelledby="boundary-heading">
          <h2 id="boundary-heading" className="section-title">Evidence boundary</h2>
          <div className="stress-grid">
            <article className="stress-card"><h4>Checked-in artifact</h4><p className="stress-detail">The proof JSON is present in the repository and its claim/run identity matches the path shown here.</p></article>
            <article className="stress-card"><h4>Digest integrity</h4><p className="stress-detail">The artifact carries a content digest that the standalone verifier can check.</p></article>
            <article className="stress-card"><h4>Not external truth</h4><p className="stress-detail">A valid proof establishes integrity and internal consistency within Habitat's evidence boundary; it does not establish publisher trust or real-world truth.</p></article>
          </div>
        </section>

        <footer className="site-footer">
          <p><a href="https://github.com/buttercode101/Habitat" target="_blank" rel="noopener noreferrer">GitHub</a> · MIT licensed · Local-first</p>
        </footer>
      </main>
    </>
  );
}
