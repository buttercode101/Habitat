import { getProof } from "../../../../../lib/habitat";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    return Response.json(await getProof(id), { headers: { "Cache-Control": "no-store" } });
  } catch {
    return Response.json({ error: "proof_unavailable" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
}
