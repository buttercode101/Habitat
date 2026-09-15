import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Habitat — Prove what your AI agents did",
  description: "Local-first accountability and portable proof for AI agents. Turn agent events into policy-checked claims you can inspect and verify.",
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    title: "Habitat — Prove what your AI agents did",
    description: "A small local-first evidence layer for AI agents.",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
