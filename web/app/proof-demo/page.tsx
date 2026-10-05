import type { Metadata } from "next";
import Link from "next/link";
import ProofDemo from "./ProofDemo";

export const metadata: Metadata = {
  title: "Habitat Proof Inspector",
  description: "Inspect the integrity of a portable Habitat proof artifact.",
};

export default function ProofDemoPage() {
  return (
    <main id="main-content" tabIndex={-1} className="shell">
      <header className="topbar">
        <Link className="brand" href="/">Habitat</Link>
        <span className="pill">PROOF INSPECTOR</span>
      </header>
      <section className="hero compact">
        <Link className="back" href="/">← Back to Habitat</Link>
        <p className="eyebrow">Independent proof surface</p>
        <h1>Inspect a Habitat proof artifact.</h1>
        <p className="lede">This page runs the artifact integrity check in your browser. No Habitat backend connection is required; external truth remains a separate assurance.</p>
      </section>
      <ProofDemo />
      <footer><Link href="/">Habitat</Link> · The artifact digest is independently verifiable in-browser.</footer>
    </main>
  );
}
