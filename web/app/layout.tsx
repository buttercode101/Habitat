import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Habitat — Agent accountability",
  description: "A small local-first accountability and proof surface for AI agents.",
  robots: {
    index: false,
    follow: false,
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
