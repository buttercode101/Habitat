type Json = Record<string, unknown>;
const MAX_RESPONSE_BYTES = 2 * 1024 * 1024;

async function boundedText(response: Response) {
  if (Number(response.headers.get("content-length")) > MAX_RESPONSE_BYTES) {
    await response.body?.cancel();
    throw new Error("backend_response_too_large");
  }
  if (!response.body) throw new Error("invalid_backend_response");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let bytes = 0, text = "";
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      if (bytes > MAX_RESPONSE_BYTES) {
        await reader.cancel();
        throw new Error("backend_response_too_large");
      }
      text += decoder.decode(value, { stream: true });
    }
    return text + decoder.decode();
  } finally { reader.releaseLock(); }
}

function baseUrl() {
  const raw = process.env.HABITAT_API_URL?.trim();
  if (!raw) throw new Error("HABITAT_API_URL is not configured");

  let url: URL;
  try {
    url = new URL(raw);
  } catch {
    throw new Error("HABITAT_API_URL is invalid");
  }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
    throw new Error("HABITAT_API_URL must be an HTTP(S) URL without credentials, query or fragment");
  }
  if (process.env.NODE_ENV === "production" && url.protocol !== "https:") {
    throw new Error("HABITAT_API_URL must use HTTPS in production");
  }
  return url.toString().replace(/\/$/, "");
}

function headers() {
  const token = process.env.HABITAT_API_TOKEN?.trim();
  if (!token) throw new Error("HABITAT_API_TOKEN is not configured");
  return { Authorization: `Bearer ${token}`, Accept: "application/json" };
}

export async function habitatFetch<T = Json>(path: string, init: RequestInit = {}): Promise<T> {
  const requestHeaders = new Headers(init.headers);
  for (const [key, value] of Object.entries(headers())) requestHeaders.set(key, value);
  const response = await fetch(`${baseUrl()}${path}`, {
    ...init,
    headers: requestHeaders,
    redirect: "error",
    signal: init.signal ?? AbortSignal.timeout(10_000),
    cache: "no-store",
  });
  if (!response.ok) {
    await response.body?.cancel();
    throw new Error(`Habitat API returned ${response.status}`);
  }
  const text = await boundedText(response);
  let payload: unknown;
  try { payload = JSON.parse(text); } catch { throw new Error("invalid_backend_response"); }
  if (!payload || typeof payload !== "object") throw new Error("invalid_backend_response");
  return payload as T;
}

export type HabitatStatus = {
  id: string;
  name: string;
  status: string;
  model?: string;
  jobs: number;
  active_signals: number;
  agents: number;
};

export type Claim = {
  id: string;
  agent_id?: string;
  run_id?: string;
  job_id?: string;
  claim?: string;
  statement?: string;
  expected_status?: string;
  status?: string;
  evidence?: unknown;
};

export async function getStatus() {
  const status = await habitatFetch<HabitatStatus>("/v1/status");
  if (Array.isArray(status) || ![status.id, status.name, status.status].every(value => typeof value === "string") ||
      ![status.jobs, status.active_signals, status.agents].every(value => Number.isSafeInteger(value) && value >= 0)) {
    throw new Error("invalid_backend_status");
  }
  return status;
}
export async function getClaims() {
  const claims = await habitatFetch<Claim[]>("/v1/claims");
  if (!Array.isArray(claims) || claims.some(claim => !claim || typeof claim.id !== "string" ||
      ["claim", "statement", "status", "agent_id", "run_id", "expected_status"].some(key => claim[key] != null && typeof claim[key] !== "string"))) {
    throw new Error("invalid_backend_claims");
  }
  return claims;
}
function object(value: unknown): value is Json {
  return !!value && typeof value === "object" && !Array.isArray(value);
}

function proofResponse(payload: Json, id: string) {
  const proof = payload.proof;
  if (payload.claim_id !== id || !object(proof) || !object(proof.claim) || proof.claim.id !== id ||
      typeof proof.claim.claim !== "string" || !object(proof.ledger) || !Array.isArray(proof.ledger.actions) ||
      typeof proof.content_sha256 !== "string" || !/^[a-f0-9]{64}$/.test(proof.content_sha256)) {
    throw new Error("invalid_backend_proof");
  }
  return payload;
}

export async function getProof(id: string) {
  return proofResponse(await habitatFetch<Json>(`/v1/claims/${encodeURIComponent(id)}/proof`), id);
}
export async function verifyClaim(id: string) {
  return proofResponse(await habitatFetch<Json>(`/v1/claims/${encodeURIComponent(id)}/verify`), id);
}
