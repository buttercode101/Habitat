"use client";

import { useState } from "react";

const steps = [
  {
    number: "01",
    title: "Get the source and install locally",
    detail: "No account or hosted control plane. The runtime and evidence database stay on your machine.",
    command: "git clone https://github.com/buttercode101/Habitat.git\ncd Habitat\npython -m pip install -e .",
  },
  {
    number: "02",
    title: "Initialize and record a sample event",
    detail: "The demo command writes explicitly labelled sample data into your local ledger.",
    command: "habitat init --config examples/simple.yaml\nhabitat demo",
  },
  {
    number: "03",
    title: "Create a portable proof",
    detail: "Bind a claim to the demo run and export a proof bundle plus a readable proof card.",
    command: "habitat prove --run-id run-42 --claim \"deployed v1.2.3 to production\" -o proof.json --card",
  },
  {
    number: "04",
    title: "Verify it independently",
    detail: "The standalone verifier checks the exported artifact without needing the producer database or a network service.",
    command: "python tools/verify_proof.py proof.json",
  },
];

export default function QuickStart() {
  const [copied, setCopied] = useState("");
  const [error, setError] = useState("");

  async function copy(label: string, value: string) {
    setCopied("");
    setError("");
    try {
      await navigator.clipboard.writeText(value);
      setCopied(label);
      window.setTimeout(() => setCopied(current => current === label ? "" : current), 1800);
    } catch {
      setError("Clipboard access is unavailable. Select and copy the command text instead.");
    }
  }

  return (
    <section className="quickstart" id="quickstart" aria-labelledby="quickstart-title">
      <div className="quickstart-heading">
        <p className="eyebrow">Start locally · no account</p>
        <h2 id="quickstart-title">From an empty folder to a verifiable proof.</h2>
        <p>Run the complete local workflow before connecting your own agent. Nothing is uploaded.</p>
      </div>
      <div className="quickstart-steps">
        {steps.map((step) => (
          <article className="quickstart-step" key={step.number}>
            <div className="quickstart-step-head">
              <span className="quickstart-number">{step.number}</span>
              <div><h3>{step.title}</h3><p>{step.detail}</p></div>
            </div>
            <pre><code>{step.command}</code></pre>
            <button className="quickstart-copy" type="button" onClick={() => copy(step.number, step.command)}>
              {copied === step.number ? "Copied" : "Copy commands"}
            </button>
          </article>
        ))}
      </div>
      <p className="quickstart-boundary"><strong>Sample-data boundary:</strong> <code>habitat demo</code> creates labelled demonstration evidence. A valid proof confirms the integrity and consistency of recorded evidence; it does not prove the example deployment happened in the outside world.</p>
      <div className="quickstart-local">
        <div className="quickstart-local-heading">
          <p className="eyebrow">Optional · local dashboard</p>
          <h3>See your local claims in the web interface.</h3>
          <p>Run the API and web UI on your own machine. Agent events, claims and proofs stay in your local Habitat database.</p>
        </div>
        <div className="quickstart-local-commands">
          <article className="quickstart-local-command">
            <span>TERMINAL 1 · HABITAT API</span>
            <pre><code>{"habitat --db .habitat/habitat.db serve --host 127.0.0.1 --port 8787"}</code></pre>
            <button className="quickstart-copy" type="button" onClick={() => copy("api", "habitat --db .habitat/habitat.db serve --host 127.0.0.1 --port 8787")}>{copied === "api" ? "Copied" : "Copy command"}</button>
          </article>
          <article className="quickstart-local-command">
            <span>TERMINAL 2 · WEB UI</span>
            <pre><code>{"cd web\nHABITAT_API_URL=http://127.0.0.1:8787 npm run dev"}</code></pre>
            <button className="quickstart-copy" type="button" onClick={() => copy("web", "cd web\nHABITAT_API_URL=http://127.0.0.1:8787 npm run dev")}>{copied === "web" ? "Copied" : "Copy commands"}</button>
          </article>
        </div>
        <p className="quickstart-local-note">Keep the API bound to <code>127.0.0.1</code>. Loopback access needs no proxy token. Do not expose the API to a network without configuring a real server secret.</p>
        <a className="quickstart-local-link" href="http://127.0.0.1:3000/dashboard">Open your local dashboard ↗</a>
      </div>
      <div className="quickstart-feedback" role="status" aria-live="polite">{copied ? "Commands copied to clipboard." : error}</div>
    </section>
  );
}
