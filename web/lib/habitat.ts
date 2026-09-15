type Json = Record<string, unknown>;

function baseUrl() {
  const raw = process.env.HABITAT_API_URL?.trim();
  if (!raw) throw new Error("HABITAT_API_URL is not configured");

  let url: URL;
  try {
    url = new URL(raw);
  } catch {
    throw new Error("HABITAT_API_URL is invalid");
  }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) {
    throw new Error("HABITAT_API_URL must be an HTTP(S) URL without embedded credentials");
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
  const response = await fetch(`${baseUrl()}${path}`, {
    ...init,
    headers: { ...(init.headers || {}), ...headers() },
    signal: init.signal ?? AbortSignal.timeout(10_000),
    cache: "no-store",
  });
  const text = await response.text();
  let payload: unknown = {};
  try { payload = text ? JSON.parse(text) : {}; } catch { payload = { error: "invalid_backend_response" }; }
  if (!response.ok) {
    const message = typeof payload === "object" && payload && "error" in payload ? String((payload as Json).error) : `Habitat API returned ${response.status}`;
    throw new Error(message);
  }
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
  statement?: string;
  expected_status?: string;
  status?: string;
  evidence?: unknown;
};

export async function getStatus() { return habitatFetch<HabitatStatus>("/v1/status"); }
export async function getClaims() { return habitatFetch<Claim[]>("/v1/claims"); }
export async function getProof(id: string) { return habitatFetch<Json>(`/v1/claims/${encodeURIComponent(id)}/proof`); }
export async function verifyClaim(id: string) { return habitatFetch<Json>(`/v1/claims/${encodeURIComponent(id)}/verify`); }
