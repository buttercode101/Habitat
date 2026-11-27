import { getProof } from "../../../../../lib/habitat";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const payload = await getProof(id);
    const filename = `habitat-proof-${id.replace(/[^a-zA-Z0-9._-]/g, "_")}.json`;
    return new Response(JSON.stringify(payload, null, 2), {
      headers: {
        "Cache-Control": "no-store",
        "Content-Disposition": `attachment; filename="${filename}"`,
        "Content-Type": "application/json; charset=utf-8",
        "X-Content-Type-Options": "nosniff",
      },
    });
  } catch {
    return Response.json({ error: "proof_unavailable" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
}
