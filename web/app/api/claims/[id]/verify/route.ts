import { verifyClaim } from "../../../../../lib/habitat";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    return Response.json(await verifyClaim(id), { headers: { "Cache-Control": "no-store" } });
  } catch {
    return Response.json({ error: "verification_failed" }, { status: 502, headers: { "Cache-Control": "no-store" } });
  }
}
