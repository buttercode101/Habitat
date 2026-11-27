export function proofDownloadResponse(payload: unknown, id: string): Response {
  const safeId = id.replace(/[^a-zA-Z0-9._-]/g, "_") || "proof";
  return new Response(JSON.stringify(payload, null, 2), {
    headers: {
      "Cache-Control": "no-store",
      "Content-Disposition": `attachment; filename="habitat-proof-${safeId}.json"`,
      "Content-Type": "application/json; charset=utf-8",
      "X-Content-Type-Options": "nosniff",
    },
  });
}
