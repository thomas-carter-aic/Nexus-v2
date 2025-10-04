import { test, expect } from '@playwright/test';

test.describe('Frontend-Backend Integration', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the dashboard
    await page.goto('/');
  });

  test('should load dashboard successfully', async ({ page }) => {
    // Check if the page loads without errors
    await expect(page).toHaveTitle(/Ultimate PaaS/);
    
    // Check for main dashboard elements
    await expect(page.locator('h1')).toContainText('Dashboard');
  });

  test('should connect to backend API', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/');
    
    // Wait for API calls to complete
    await page.waitForLoadState('networkidle');
    
    // Check for data that would come from backend
    const statsCards = page.locator('[data-testid="stats-card"]');
    await expect(statsCards).toHaveCount(4);
  });

  test('should handle authentication flow', async ({ page }) => {
    // If not authenticated, should show login prompt
    const loginButton = page.locator('button:has-text("Sign In")');
    
    if (await loginButton.isVisible()) {
      await loginButton.click();
      
      // Should navigate to auth page or show auth modal
      await expect(page.locator('input[type="email"], input[type="text"]')).toBeVisible();
    }
  });

  test('should navigate between microfrontends', async ({ page }) => {
    // Test navigation to different microfrontends
    const services = [
      'Application Management',
      'Deployment Center', 
      'AI Analytics',
      'Plugin Management',
      'Security Center',
      'Monitoring'
    ];

    for (const service of services) {
      const serviceCard = page.locator(`text=${service}`).first();
      if (await serviceCard.isVisible()) {
        const openButton = serviceCard.locator('..').locator('button:has-text("Open Service")');
        await expect(openButton).toBeVisible();
      }
    }
  });

  test('should display real-time data', async ({ page }) => {
    // Navigate to monitoring or dashboard
    await page.goto('/');
    
    // Wait for initial load
    await page.waitForLoadState('networkidle');
    
    // Check for elements that would show real-time data
    const metricsElements = page.locator('[data-testid*="metric"], [data-testid*="chart"]');
    
    // Should have some metrics displayed
    const count = await metricsElements.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API failure
    await page.route('**/api/**', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      });
    });

    await page.goto('/');
    
    // Should show error state or fallback UI
    await expect(page.locator('text=Error, text=Failed, text=Unable')).toBeVisible();
  });
});

test.describe('Cross-Browser Compatibility', () => {
  test('should work consistently across browsers', async ({ page, browserName }) => {
    await page.goto('/');
    
    // Basic functionality should work in all browsers
    await expect(page.locator('h1')).toBeVisible();
    
    // Check for browser-specific issues
    if (browserName === 'webkit') {
      // Safari-specific checks
      await expect(page.locator('body')).toHaveCSS('font-family', /system-ui/);
    }
  });
});

test.describe('Performance', () => {
  test('should load within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Should load within 5 seconds
    expect(loadTime).toBeLessThan(5000);
  });

  test('should not have console errors', async ({ page }) => {
    const consoleErrors: string[] = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Filter out known acceptable errors
    const criticalErrors = consoleErrors.filter(error => 
      !error.includes('favicon') && 
      !error.includes('404') &&
      !error.includes('net::ERR_FAILED')
    );
    
    expect(criticalErrors).toHaveLength(0);
  });
});
