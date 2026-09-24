import Link from "next/link";
import ProofDemo from "./ProofDemo";

export const metadata = {
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
      <ProofDemo />
    </main>
  );
}
