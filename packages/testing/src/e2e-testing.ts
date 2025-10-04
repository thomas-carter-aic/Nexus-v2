import { test, expect, Page, Browser } from '@playwright/test';

/**
 * End-to-End Testing Utilities
 * 
 * Playwright-based E2E tests for full user workflows
 */

export class E2ETestSuite {
  private page: Page;
  private baseUrl: string;

  constructor(page: Page, baseUrl: string = 'http://localhost:3000') {
    this.page = page;
    this.baseUrl = baseUrl;
  }

  /**
   * Test complete user authentication flow
   */
  async testAuthenticationFlow() {
    await this.page.goto(`${this.baseUrl}/login`);
    
    // Fill login form
    await this.page.fill('[data-testid="username"]', 'admin');
    await this.page.fill('[data-testid="password"]', 'admin123');
    
    // Submit login
    await this.page.click('[data-testid="login-button"]');
    
    // Wait for redirect to dashboard
    await this.page.waitForURL(`${this.baseUrl}/dashboard`);
    
    // Verify user is logged in
    await expect(this.page.locator('[data-testid="user-menu"]')).toBeVisible();
  }

  /**
   * Test application management workflow
   */
  async testApplicationManagement() {
    // Navigate to app management
    await this.page.goto(`${this.baseUrl}/app-management`);
    
    // Create new application
    await this.page.click('[data-testid="create-app-button"]');
    
    // Fill application form
    await this.page.fill('[data-testid="app-name"]', 'E2E Test App');
    await this.page.fill('[data-testid="app-description"]', 'Created by E2E test');
    await this.page.fill('[data-testid="repo-url"]', 'https://github.com/test/e2e-app');
    
    // Submit form
    await this.page.click('[data-testid="submit-app"]');
    
    // Wait for success message
    await expect(this.page.locator('[data-testid="success-message"]')).toBeVisible();
    
    // Verify app appears in list
    await expect(this.page.locator('text=E2E Test App')).toBeVisible();
  }

  /**
   * Test deployment workflow
   */
  async testDeploymentWorkflow() {
    // Navigate to deployment page
    await this.page.goto(`${this.baseUrl}/deployment`);
    
    // Select application to deploy
    await this.page.selectOption('[data-testid="app-selector"]', 'E2E Test App');
    
    // Configure deployment
    await this.page.selectOption('[data-testid="environment-selector"]', 'staging');
    await this.page.selectOption('[data-testid="strategy-selector"]', 'blue_green');
    
    // Start deployment
    await this.page.click('[data-testid="deploy-button"]');
    
    // Wait for deployment to start
    await expect(this.page.locator('[data-testid="deployment-status"]')).toContainText('Running');
    
    // Wait for deployment to complete (with timeout)
    await this.page.waitForSelector('[data-testid="deployment-success"]', { timeout: 60000 });
  }

  /**
   * Test AI analytics dashboard
   */
  async testAIAnalytics() {
    await this.page.goto(`${this.baseUrl}/ai-analytics`);
    
    // Wait for charts to load
    await this.page.waitForSelector('[data-testid="performance-chart"]');
    await this.page.waitForSelector('[data-testid="cost-chart"]');
    
    // Verify insights are displayed
    await expect(this.page.locator('[data-testid="ai-insights"]')).toBeVisible();
    
    // Test filtering
    await this.page.selectOption('[data-testid="time-range-filter"]', '7d');
    
    // Wait for charts to update
    await this.page.waitForTimeout(2000);
  }

  /**
   * Test cross-microfrontend navigation
   */
  async testMicrofrontendNavigation() {
    // Start at dashboard
    await this.page.goto(`${this.baseUrl}/dashboard`);
    
    // Navigate to each microfrontend
    const microfrontends = [
      { name: 'App Management', port: 3001 },
      { name: 'Deployment', port: 3002 },
      { name: 'AI Analytics', port: 3003 },
      { name: 'Plugin Management', port: 3004 },
      { name: 'Security', port: 3005 },
      { name: 'Monitoring', port: 3006 },
    ];

    for (const mf of microfrontends) {
      // Click navigation link
      await this.page.click(`[data-testid="nav-${mf.name.toLowerCase().replace(' ', '-')}"]`);
      
      // Verify navigation (either same tab or new tab)
      const currentUrl = this.page.url();
      expect(currentUrl).toContain(`localhost:${mf.port}`);
      
      // Go back to dashboard
      await this.page.goto(`${this.baseUrl}/dashboard`);
    }
  }

  /**
   * Test responsive design
   */
  async testResponsiveDesign() {
    await this.page.goto(`${this.baseUrl}/dashboard`);
    
    // Test mobile viewport
    await this.page.setViewportSize({ width: 375, height: 667 });
    
    // Verify mobile menu is visible
    await expect(this.page.locator('[data-testid="mobile-menu-button"]')).toBeVisible();
    
    // Test tablet viewport
    await this.page.setViewportSize({ width: 768, height: 1024 });
    
    // Test desktop viewport
    await this.page.setViewportSize({ width: 1920, height: 1080 });
    
    // Verify desktop layout
    await expect(this.page.locator('[data-testid="desktop-sidebar"]')).toBeVisible();
  }

  /**
   * Test error handling
   */
  async testErrorHandling() {
    // Test 404 page
    await this.page.goto(`${this.baseUrl}/non-existent-page`);
    await expect(this.page.locator('text=404')).toBeVisible();
    
    // Test API error handling
    // This would require mocking API failures
  }
}

// Playwright test configurations
export const playwrightConfig = {
  testDir: './e2e',
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...require('@playwright/test').devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...require('@playwright/test').devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...require('@playwright/test').devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...require('@playwright/test').devices['Pixel 5'] },
    },
  ],
  webServer: [
    {
      command: 'npm run dev',
      port: 3000,
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'cd ../ultimate-paas-base && python src/main.py',
      port: 8000,
      reuseExistingServer: !process.env.CI,
    },
  ],
};
