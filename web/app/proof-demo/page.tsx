import type { Metadata } from "next";
import Link from "next/link";
import ProofDemo from "./ProofDemo";

export const metadata: Metadata = {
  title: "Habitat Proof Inspector",
  description: "Inspect and verify a portable Habitat proof.",
};

export default function ProofDemoPage() {
  return (
    <main className="shell">
      <header className="topbar">
        <Link className="brand" href="/">Habitat</Link>
        <span className="pill">PROOF INSPECTOR</span>
      </header>
      <section className="hero compact">
        <Link className="back" href="/">← Back to Habitat</Link>
        <p className="eyebrow">Independent proof surface</p>
        <h1>Inspect and verify a real Habitat proof.</h1>
        <p className="lede">This page runs the proof check in your browser. No Habitat backend connection is required.</p>
      </section>
      <ProofDemo />
      <footer><Link href="/">Habitat</Link> · The proof is independently verifiable in-browser.</footer>
    </main>
  );
}
