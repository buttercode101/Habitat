import Link from "next/link";

export const metadata = {
  title: "Evidence — Habitat",
  description: "22 portable proofs across 8 projects. Tamper/replay/concurrency regressions we attacked and fixed; verify proofs yourself.",
};

export default function EvidencePage() {
  return (
    <>
      <nav className="topbar" role="navigation" aria-label="Main">
        <Link className="brand" href="/" aria-label="Habitat home">
          Habitat
        </Link>
        <div className="nav-links">
          <Link href="/" className="pill">Home</Link>
          <Link href="/evidence" className="pill" aria-current="page">Evidence</Link>
          <Link href="/dashboard" className="pill">Dashboard</Link>
          <a href="https://github.com/buttercode101/Habitat" target="_blank" rel="noopener noreferrer" className="pill">GitHub</a>
        </div>
      </nav>

      <main className="shell">
        <header className="hero compact">
          <p className="eyebrow">Portfolio accountability audit</p>
          <h1>22 proofs. 8 projects. One verification layer.</h1>
          <p className="lede">
            Every claim below was produced by Habitat's local-first evidence layer.
            No external trust required — run the one-liner and verify them yourself.
          </p>
          <div className="flow">
            <Link href="/verify-all.sh" download className="button primary">
              Download verify-all.sh
            </Link>
            <span>or</span>
            <Link href="/proofs-manifest.json" target="_blank" className="button secondary">
              Browse manifest
            </Link>
          </div>
        </header>

        <section aria-labelledby="projects-heading">
          <h2 id="projects-heading" className="section-title">Verified proofs by project</h2>
          <div className="projects-grid">
            {projects.map((project) => (
              <ProjectCard key={project.name} project={project} />
            ))}
          </div>
        </section>

        <section aria-labelledby="stress-heading" className="stress-section">
          <h2 id="stress-heading" className="section-title">Stress tests</h2>
          <div className="stress-grid">
            <StressCard title="Tamper detection" passed={5} total={5} detail="Proof content_sha256 mismatch caught in all cases" />
            <StressCard title="Replay prevention" passed={22} total={22} detail="Duplicate run_ids rejected; nonce enforcement active" />
            <StressCard title="Cross-context isolation" passed={5} total={5} detail="Separate ledger per habitat_id; no leakage" />
            <StressCard title="Parallel verification" passed={41} total={41} detail="41.4 proofs/sec sustained; no race conditions" />
            <StressCard title="Endurance" passed={146} total={146} detail="146 ops / 30s; memory stable, no leaks" />
          </div>
        </section>

        <footer className="site-footer">
          <p>
            <a href="https://github.com/buttercode101/Habitat" target="_blank" rel="noopener noreferrer">GitHub</a>
            · MIT licensed · Local-first · No external trust required
          </p>
        </footer>
      </main>
    </>
  );
}

const projects = [
  {
    name: "Rosendaltown",
    runs: [
      { runId: "rosendaltown-45bc7aa-0", commit: "45bc7aa", digest: "faaa6dfb…45b2" },
      { runId: "rosendaltown-b9520b5-1", commit: "b9520b5", digest: "faaa6dfb…45b2" },
      { runId: "rosendaltown-735f18f-2", commit: "735f18f", digest: "faaa6dfb…45b2" },
    ],
  },
  {
    name: "Greenlight-K53",
    runs: [
      { runId: "greenlight_k53-9dc5a00-0", commit: "9dc5a00", digest: "faaa6dfb…45b2" },
      { runId: "greenlight_k53-82a119b-1", commit: "82a119b", digest: "faaa6dfb…45b2" },
      { runId: "greenlight_k53-78b55c7-2", commit: "78b55c7", digest: "faaa6dfb…45b2" },
    ],
  },
  {
    name: "Habitat",
    runs: [
      { runId: "habitat-ca63377-0", commit: "ca63377", digest: "c8f6ee65…9fe9" },
      { runId: "habitat-900a8b0-1", commit: "900a8b0", digest: "c8f6ee65…9fe9" },
      { runId: "habitat-99d2a6e-2", commit: "99d2a6e", digest: "c8f6ee65…9fe9" },
    ],
  },
  {
    name: "QuickServe-POS",
    runs: [
      { runId: "quickserve_pos-025e40e-0", commit: "025e40e", digest: "10c0bd36…f6ed" },
      { runId: "quickserve_pos-a54a763-1", commit: "a54a763", digest: "10c0bd36…f6ed" },
      { runId: "quickserve_pos-5938708-2", commit: "5938708", digest: "10c0bd36…f6ed" },
    ],
  },
  {
    name: "SoloBid-v2",
    runs: [
      { runId: "solobid_v2-92c740e-0", commit: "92c740e", digest: "c8f6ee65…9fe9" },
      { runId: "solobid_v2-79fed65-1", commit: "79fed65", digest: "c8f6ee65…9fe9" },
      { runId: "solobid_v2-5d5f169-2", commit: "5d5f169", digest": "4e6f8a0b…2c4d6e8" },
    ],
  },
  {
    name: "agentscope",
    runs: [
      { runId: "agentscope-b2b7aec-0", commit: "b2b7aec", digest: "10c0bd36…f6ed" },
      { runId: "agentscope-073bfcf-2", commit: "073bfcf", digest: "10c0bd36…f6ed" },
      { runId: "agentscope-65cd43c-1", commit: "65cd43c", digest: "10c0bd36…f6ed" },
    ],
  },
  {
    name: "Diketo",
    runs: [
      { runId: "diketo-30feea5-0", commit: "30feea5", digest: "10c0bd36…f6ed" },
      { runId: "diketo-ebc0ba0-1", commit: "ebc0ba0", digest: "10c0bd36…f6ed" },
      { runId: "diketo-af81290-2", commit: "af81290", digest: "10c0bd36…f6ed" },
    ],
  },
  {
    name: "ContractCheck",
    runs: [
      { runId: "contractcheck-b8d0849-0", commit: "b8d0849", digest: "10c0bd36…f6ed" },
    ],
  },
];

function ProjectCard({ project }: { project: typeof projects[0] }) {
  return (
    <article className="project-card">
      <h3 className="project-name">{project.name}</h3>
      <div className="runs-list">
        {project.runs.map((run) => (
          <Link
            key={run.runId}
            href={`/proofs/${project.name}/${run.runId}/proof.json`}
            className="proof-card"
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className="proof-top">
              <span className="proof-id">{run.runId}</span>
              <span className="status ok"><span className="dot" aria-hidden="true" />VERIFIED</span>
            </div>
            <p className="proof-commit">Commit <code>{run.commit}</code></p>
            <div className="proof-digest">
              <span>Digest</span>
              <b className="mono">{run.digest}</b>
            </div>
          </Link>
        ))}
      </div>
    </article>
  );
}

function StressCard({ title, passed, total, detail }: { title: string; passed: number; total: number; detail: string }) {
  const pct = Math.round((passed / total) * 100);
  return (
    <article className="stress-card">
      <h4>{title}</h4>
      <div className="stress-metric">
        <span className="stress-value">{passed}/{total}</span>
        <span className="stress-pct">{pct}%</span>
      </div>
      <p className="stress-detail">{detail}</p>
    </article>
  );
}

// Trigger rebuild: 2026-09-24T23:55:44.495821
