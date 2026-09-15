import "./globals.css";

export const metadata = {
  title: "Habitat — Agent accountability",
  description: "A small local-first accountability and proof surface for AI agents.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
