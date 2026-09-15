import { getProof } from "../../../../../../lib/habitat";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    return Response.json(await getProof(id), { headers: { "Cache-Control": "no-store" } });
  } catch (error) {
    return Response.json({ error: error instanceof Error ? error.message : "proof_unavailable" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
}
