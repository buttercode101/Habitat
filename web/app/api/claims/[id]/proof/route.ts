import { getProof } from "../../../../../lib/habitat";
import { proofDownloadResponse } from "../../../../../lib/proof-download";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    return proofDownloadResponse(await getProof(id), id);
  } catch {
    return Response.json({ error: "proof_unavailable" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
}
