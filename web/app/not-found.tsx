import Link from "next/link";

export default function NotFound() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        padding: "32px",
        background: "#f4f4ef",
        color: "#11110f",
        fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
      }}
    >
      <section style={{ width: "min(620px, 100%)" }}>
        <p style={{ fontSize: 12, letterSpacing: ".12em", textTransform: "uppercase", opacity: .55 }}>
          Habitat / 404
        </p>
        <h1 style={{ fontSize: "clamp(42px, 8vw, 76px)", lineHeight: .95, letterSpacing: "-.06em", margin: "14px 0 20px" }}>
          This proof path does not exist.
        </h1>
        <p style={{ maxWidth: 520, lineHeight: 1.7, color: "#5e605a" }}>
          The requested page is not part of the verified Habitat web surface.
        </p>
        <Link
          href="/"
          style={{
            display: "inline-flex",
            marginTop: 24,
            minHeight: 48,
            alignItems: "center",
            padding: "0 16px",
            borderRadius: 9,
            background: "#11110f",
            color: "#fff",
            textDecoration: "none",
            fontWeight: 700,
          }}
        >
          Back to Habitat
        </Link>
      </section>
    </main>
  );
}
