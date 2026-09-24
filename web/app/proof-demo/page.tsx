import { redirect } from "next/navigation";

export const metadata = {
  title: "Habitat Proof Inspector",
  description: "Inspect and verify a portable Habitat proof.",
};

export default function ProofDemoPage() {
  redirect("/dashboard#proof-demo");
}
