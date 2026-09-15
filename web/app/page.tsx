import Link from "next/link";

const GITHUB_URL = "https://github.com/buttercode101/Habitat";
const PROOF_URL = "https://github.com/buttercode101/Habitat/blob/main/proofs/rosendaltown-45bc7aa7.json";

export default function Home() {
  return (
    <main className="marketing-shell">
      <header className="marketing-nav shell-width">
        <Link className="brand" href="/">Habitat</Link>
        <nav className="desktop-nav" aria-label="Primary navigation">
          <a href="#how-it-works">How it works</a>
          <a href="#why">Why Habitat</a>
          <Link href="/dashboard">Live dashboard</Link>
          <a className="nav-cta" href={GITHUB_URL}>GitHub ↗</a>
        </nav>
        <details className="mobile-nav">
          <summary aria-label="Open navigation"><span>Menu</span><i aria-hidden="true">↗</i></summary>
          <div className="mobile-nav-panel">
            <a href="#how-it-works">How it works</a>
            <a href="#why">Why Habitat</a>
            <Link href="/dashboard">Live dashboard</Link>
            <a href={GITHUB_URL}>GitHub ↗</a>
          </div>
        </details>
      </header>

      <section className="marketing-hero shell-width">
        <div className="hero-copy">
          <p className="eyebrow">Accountability for AI agents</p>
          <h1>Don&apos;t just log what an agent did. <em>Prove it.</em></h1>
          <p className="marketing-lede">Habitat turns agent events into policy-checked claims and portable proof artifacts you can inspect, verify and carry outside the system that produced them.</p>
          <div className="hero-actions">
            <a className="button primary large" href={GITHUB_URL}>Get Habitat on GitHub ↗</a>
            <a className="button large" href={PROOF_URL}>See a real proof ↗</a>
          </div>
          <p className="hero-note">Local-first · portable · no hosted control plane required</p>
        </div>
        <div className="hero-proof" aria-label="Habitat proof flow">
          <div className="proof-window">
            <div className="window-bar"><span /><span /><span /><b>habitat proof</b></div>
            <div className="proof-status"><span className="status-dot" /> VERIFIED <small>portable proof</small></div>
            <div className="proof-claim">Rosendaltown change <strong>45bc7aa7</strong> has a verified evidence trail.</div>
            <div className="proof-live"><span className="live-dot" /><strong>VERIFIED</strong><span>Habitat ledger · exact run correlation</span></div>
            <div className="proof-lines">
              <div><span>Evidence</span><b>trusted ledger</b></div>
              <div><span>Action</span><b>repository change</b></div>
              <div><span>Integrity</span><b>intact</b></div>
              <div><span>Digest</span><b className="mono">a21b7f2f…18fc088</b></div>
            </div>
            <div className="proof-footer">structural · integrity · consistency</div>
          </div>
        </div>
      </section>

      <section className="trust-strip"><div className="shell-width trust-inner"><span>Built for the gap between</span><strong>observability</strong><i>and</i><strong>trust</strong></div></section>

      <section className="marketing-section shell-width" id="how-it-works">
        <div className="section-intro"><p className="eyebrow">The protocol</p><h2>A small evidence layer for the agents you already run.</h2><p>Habitat does not replace your traces, logs, orchestration or model stack. It sits beside them and records the evidence that matters.</p></div>
        <div className="steps">
          <Step n="01" title="Capture" text="Receive the events your agents already emit and bind them to an identity and run." />
          <Step n="02" title="Check" text="Apply policy and authorization before an action becomes trusted evidence." />
          <Step n="03" title="Correlate" text="Connect claims to the exact run, job and action instead of guessing from recent history." />
          <Step n="04" title="Prove" text="Export a portable proof bundle that can be independently verified outside Habitat." />
        </div>
      </section>

      <section className="dark-section" id="why">
        <div className="shell-width split-section">
          <div><p className="eyebrow">Why this exists</p><h2>Logs tell you what was recorded. Proof tells you what the evidence supports.</h2></div>
          <div className="split-copy"><p>AI agents increasingly act across systems, make decisions and touch shared state. A dashboard can show activity. It cannot by itself establish that a specific claim was authorized, correlated to the right action, or preserved without tampering.</p><p>Habitat keeps that boundary deliberately narrow: cryptographic integrity and evidence consistency are explicit, while publisher trust and real-world truth remain separate assurances.</p></div>
        </div>
      </section>

      <section className="marketing-section shell-width">
        <div className="section-intro"><p className="eyebrow">Use it where the action matters</p><h2>From agent runs to consequential changes.</h2></div>
        <div className="use-grid">
          <UseCase title="Production changes" text="Attach proof to deployments, promotions and other shared-state changes." />
          <UseCase title="Agent workflows" text="Verify that an agent performed the action it was expected and authorized to perform." />
          <UseCase title="CI / automation" text="Carry evidence from an automated run into a PR, issue, ticket or handoff." />
          <UseCase title="Audits & handoffs" text="Give another person or system a compact artifact they can verify independently." />
        </div>
      </section>

      <section className="boundary shell-width">
        <div><p className="eyebrow">Trust, without overclaiming</p><h2>Every proof has a boundary.</h2></div>
        <div className="assurance-list">
          <div><strong>✓ Structural validity</strong><span>The proof matches the expected schema.</span></div>
          <div><strong>✓ Content integrity</strong><span>The proof content matches its digest.</span></div>
          <div><strong>✓ Internal consistency</strong><span>Claims, runs, actions and evidence agree.</span></div>
          <div><strong>— Publisher trust</strong><span>Requires a trusted identity and key.</span></div>
          <div><strong>— External truth</strong><span>A valid proof does not magically establish what happened in the physical world.</span></div>
        </div>
      </section>

      <section className="final-cta shell-width">
        <p className="eyebrow">Start small</p>
        <h2>Give one consequential agent action a proof.</h2>
        <p>Run Habitat beside the systems you already use. Keep the ledger local. Export the evidence when you need to share it.</p>
        <div className="hero-actions"><a className="button primary large" href={GITHUB_URL}>Get started on GitHub ↗</a><Link className="button large" href="/dashboard">Open dashboard</Link></div>
      </section>

      <footer className="marketing-footer shell-width"><Link className="brand" href="/">Habitat</Link><span>Local-first accountability for AI agents.</span><a href={GITHUB_URL}>GitHub ↗</a></footer>
    </main>
  );
}

function Step({ n, title, text }: { n: string; title: string; text: string }) {
  return <article className="step"><span>{n}</span><h3>{title}</h3><p>{text}</p></article>;
}

function UseCase({ title, text }: { title: string; text: string }) {
  return <article className="use-card"><h3>{title}</h3><p>{text}</p></article>;
}
