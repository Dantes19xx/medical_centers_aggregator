/**
 * Playwright test runner configuration — Medical Clinic Aggregator
 *
 * Spec files live in frontend/tests/e2e/.
 * CI entry point (devops_engineer.md — frontend-ci.yml):
 *   npm run preview &
 *   sleep 3
 *   npx playwright test
 *
 * Local:
 *   npx playwright test           — run all specs
 *   npx playwright test --ui      — visual test runner
 *   npx playwright test --headed  — watch browser
 *
 * Environment variables:
 *   BASE_URL   — override the app base URL (default: http://localhost:3000)
 *   CI         — set by GitHub Actions; enables stricter retry/worker config
 *
 * TODO (frontend_developer): the webServer command below starts the Vite dev
 * server. Update the command if the frontend start script changes.
 */

import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",

  // Fail the build in CI if you accidentally left test.only in source
  forbidOnly: !!process.env.CI,

  // Retry flaky tests twice in CI; no retries locally
  retries: process.env.CI ? 2 : 0,

  // Single worker in CI to avoid race conditions on shared DB/port;
  // full parallelism locally
  workers: process.env.CI ? 1 : undefined,
  fullyParallel: !process.env.CI,

  reporter: [
    ["html", { outputFolder: "playwright-report", open: "never" }],
    ["list"],
    // Uncomment for GitHub Actions annotations:
    // ["github"],
  ],

  use: {
    // All pages in specs resolve relative to this origin.
    // Frontend runs on port 3000 (frontend_developer.md + devops docker-compose).
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",

    // Attach screenshots / videos only on failure to keep CI artifacts small
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    trace: "on-first-retry",

    // Default navigation timeout (ms)
    navigationTimeout: 15_000,
    actionTimeout: 10_000,
  },

  // Projects = browser matrix.
  // Add webkit / firefox once E2E tests are stable.
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    // {
    //   name: "firefox",
    //   use: { ...devices["Desktop Firefox"] },
    // },
    // {
    //   name: "mobile-chrome",
    //   use: { ...devices["Pixel 5"] },
    // },
  ],

  // Automatically start the dev server before running specs.
  // reuseExistingServer lets you keep `npm run dev` open locally without
  // Playwright spawning a second one.
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    // Silence noisy Vite output in CI
    stdout: process.env.CI ? "ignore" : "pipe",
    stderr: "pipe",
  },
});
