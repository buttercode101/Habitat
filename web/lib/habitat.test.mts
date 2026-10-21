import { test } from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { getStatus, getClaims, habitatFetch } from "./habitat.ts";

test("real HTTP upstream failures cannot become live dashboard data", async () => {
  const original = { url: process.env.HABITAT_API_URL, token: process.env.HABITAT_API_TOKEN };
  const seen: string[] = [];
  const server = createServer((req, res) => {
    seen.push(req.url!);
    assert.equal(req.headers.authorization, "Bearer synthetic-test-token");
    if (req.url === "/malformed") return res.end("<html>maintenance</html>");
    if (req.url === "/empty") return res.end();
    if (req.url === "/redirect") { res.writeHead(302, { Location: "/target" }); return res.end(); }
    if (req.url === "/error") { res.writeHead(503); return res.end(JSON.stringify({ error: "sensitive upstream detail" })); }
    if (req.url === "/v1/status") return res.end(JSON.stringify({ id: "h", name: "test", status: "active", jobs: 0, agents: 1, active_signals: 0 }));
    if (req.url === "/v1/claims") return res.end(JSON.stringify([{ id: "c", claim: "Python claim field", job_id: null, run_id: null, status: "pending" }]));
    res.end(JSON.stringify({ error: "wrong schema" }));
  });
  await new Promise<void>(resolve => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as { port: number };
  process.env.HABITAT_API_URL = `http://127.0.0.1:${address.port}`;
  process.env.HABITAT_API_TOKEN = "synthetic-test-token";
  try {
    assert.equal((await getStatus()).agents, 1);
    assert.equal((await getClaims())[0].claim, "Python claim field");
    for (const path of ["/malformed", "/empty"]) await assert.rejects(habitatFetch(path), /invalid_backend_response/);
    await assert.rejects(habitatFetch("/redirect"));
    assert.ok(!seen.includes("/target"), "must not follow credentialed redirects");
    await assert.rejects(habitatFetch("/error"), { message: "Habitat API returned 503" });
    process.env.HABITAT_API_URL += "/wrong-prefix";
    await assert.rejects(getStatus(), /invalid_backend_status/);
    await assert.rejects(getClaims(), /invalid_backend_claims/);
    process.env.HABITAT_API_URL += "?bad=1";
    await assert.rejects(getStatus(), /HABITAT_API_URL/);
  } finally {
    for (const [key, value] of [["HABITAT_API_URL", original.url], ["HABITAT_API_TOKEN", original.token]]) {
      if (value === undefined) delete process.env[key!]; else process.env[key!] = value;
    }
    await new Promise<void>((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  }
});
