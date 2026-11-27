import { defineConfig } from '@playwright/test';

const port = 3210;
const fallbackPort = 3213;

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: 'list',
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    browserName: 'chromium',
    headless: true,
    permissions: ['clipboard-read', 'clipboard-write'],
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command: 'bash e2e/start-habitat-api.sh',
      url: 'http://127.0.0.1:8787/healthz',
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
    {
      command: `HABITAT_API_URL=http://127.0.0.1:8787 HABITAT_API_TOKEN=local-only npm run start -- --hostname 127.0.0.1 --port ${port}`,
      url: `http://127.0.0.1:${port}`,
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
    {
      command: `npm run start -- --hostname 127.0.0.1 --port ${fallbackPort}`,
      url: `http://127.0.0.1:${fallbackPort}`,
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
  ],
});
