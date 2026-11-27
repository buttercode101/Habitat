import { expect, test } from '@playwright/test';

test('local quickstart copies real commands and discloses sample evidence', async ({ page }) => {
  const response = await page.goto('/');
  expect(response?.status()).toBe(200);
  await expect(page.getByRole('heading', { name: 'From an empty folder to a verifiable proof.' })).toBeVisible();
  await expect(page.getByText(/Sample-data boundary/)).toBeVisible();
  await page.getByRole('button', { name: 'Copy commands' }).first().click();
  await expect(page.getByText('Commands copied to clipboard.')).toBeVisible();
  const copied = await page.evaluate(() => navigator.clipboard.readText());
  expect(copied).toContain('git clone https://github.com/buttercode101/Habitat.git');
  expect(copied).toContain('python -m pip install -e .');
  await expect(page.getByRole('heading', { name: 'See your local claims in the web interface.' })).toBeVisible();
  await page.getByRole('button', { name: 'Copy commands' }).last().click();
  const localWebCommand = await page.evaluate(() => navigator.clipboard.readText());
  expect(localWebCommand).toContain('HABITAT_API_URL=http://127.0.0.1:8787');
  await expect(page.getByRole('link', { name: 'Open your local dashboard' })).toHaveAttribute('href', 'http://127.0.0.1:3000/dashboard');
});

test('proof inspector verifies, detects tampering, resets and exports', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:3213/dashboard');
  expect(response?.status()).toBe(200);
  await expect(page.getByText('DEMO MODE').first()).toBeVisible();
  await expect(page.getByText('Live backend unavailable').first()).toBeVisible();
  const verify = page.getByRole('button', { name: 'Verify proof' });
  await verify.click();
  await expect(page.getByText(/DIGEST MATCHES/).first()).toBeVisible();
  await page.getByRole('button', { name: 'Simulate tampering' }).click();
  await expect(page.getByText('TAMPERED').first()).toBeVisible();
  await verify.click();
  await expect(page.getByText('DIGEST MISMATCH').first()).toBeVisible();
  await page.getByRole('button', { name: 'Reset' }).click();
  await expect(page.getByText('READY').first()).toBeVisible();
  await verify.click();
  await expect(page.getByText(/DIGEST MATCHES/).first()).toBeVisible();
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download JSON' }).click();
  expect((await downloadPromise).suggestedFilename()).toBe('habitat-proof-rosendaltown.json');
});


test('local Habitat API powers real claims, verification and proof downloads', async ({ page }) => {
  const response = await page.goto('/dashboard');
  expect(response?.status()).toBe(200);
  await expect(page.getByText('LIVE ACCOUNTABILITY SURFACE').first()).toBeVisible();
  await expect(page.getByText('deployed v1.2.3 to production').first()).toBeVisible();
  await expect(page.getByText('Sample evidence detected')).toBeVisible();
  await expect(page.getByText(/SAMPLE · verified/i).first()).toBeVisible();

  await page.getByRole('button', { name: 'Verify now' }).first().click();
  await expect(page.getByText('Verifier response: verified').first()).toBeVisible();
  await expect(page.getByText('Ledger integrity: intact').first()).toBeVisible();

  await page.getByRole('link', { name: 'Inspect claim' }).click();
  await expect(page.getByText('Sample data — not live activity')).toBeVisible();
  await page.getByRole('button', { name: 'Verify now' }).click();
  await expect(page.getByText('Verifier response: verified')).toBeVisible();

  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('link', { name: 'Download proof JSON' }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toMatch(/^habitat-proof-[a-f0-9-]+\.json$/);
});

test('all public routes fit phone, tablet and desktop widths', async ({ page }) => {
  test.setTimeout(90_000);
  const widths = [320, 360, 375, 390, 430, 768, 1024, 1440];
  const routes = ['/', '/dashboard', '/evidence', '/proof-demo'];
  const pageErrors: string[] = [];
  page.on('pageerror', error => pageErrors.push(error.message));
  for (const route of routes) for (const width of widths) {
    await page.setViewportSize({ width, height: 900 });
    const response = await page.goto(route);
    expect(response?.status(), `${route} at ${width}px`).toBe(200);
    const dimensions = await page.evaluate(() => ({ document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
    expect(dimensions.document, `${route} horizontal overflow at ${width}px`).toBeLessThanOrEqual(width + 1);
    expect(dimensions.body, `${route} body overflow at ${width}px`).toBeLessThanOrEqual(width + 1);
  }
  expect(pageErrors).toEqual([]);
});

test('mobile navigation and reduced-motion preferences are respected', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  const navigation = page.locator('.mobile-nav');
  await navigation.locator('summary').click();
  await expect(navigation.locator('.mobile-nav-panel')).toBeVisible();
  await page.emulateMedia({ reducedMotion: 'reduce' });
  const transition = await page.locator('.quickstart-copy').first().evaluate(element => getComputedStyle(element).transitionDuration);
  expect(transition).toBe('0s');
});
