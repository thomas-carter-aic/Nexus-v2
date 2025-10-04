import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode } from 'react';

/**
 * Integration Testing Utilities
 * 
 * Utilities for testing React components with backend integration
 */

// Test wrapper with providers
export function createTestWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        staleTime: 0,
        gcTime: 0,
      },
    },
  });

  return function TestWrapper({ children }: { children: ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  };
}

// Custom render function with providers
export function renderWithProviders(ui: ReactNode) {
  const Wrapper = createTestWrapper();
  return render(ui, { wrapper: Wrapper });
}

// Wait for API calls to complete
export async function waitForApiCall(timeout = 5000) {
  await waitFor(() => {
    // Wait for any pending API calls
  }, { timeout });
}

// Mock user authentication
export function mockAuthenticatedUser() {
  const mockUser = {
    id: 'test-user-id',
    email: 'test@example.com',
    name: 'Test User',
    role: 'developer',
    permissions: [
      { resource: 'applications', actions: ['read', 'write'] },
      { resource: 'deployments', actions: ['read', 'write'] },
    ],
  };

  // Mock the auth store
  jest.mock('@ultimate-paas/auth', () => ({
    useAuthStore: () => ({
      user: mockUser,
      isAuthenticated: true,
      hasPermission: (resource: string, action: string) => {
        const permission = mockUser.permissions.find(p => p.resource === resource);
        return permission?.actions.includes(action) || false;
      },
      hasRole: (role: string) => mockUser.role === role,
    }),
  }));

  return mockUser;
}

// Integration test scenarios
export class IntegrationTestScenarios {
  /**
   * Test application creation flow
   */
  static async testApplicationCreation() {
    const user = userEvent.setup();
    
    // This would be implemented with actual components
    // render(<ApplicationCreateForm />);
    
    // Fill form
    // await user.type(screen.getByLabelText(/application name/i), 'Test App');
    // await user.type(screen.getByLabelText(/description/i), 'Test Description');
    // await user.type(screen.getByLabelText(/repository url/i), 'https://github.com/test/repo');
    
    // Submit form
    // await user.click(screen.getByRole('button', { name: /create application/i }));
    
    // Wait for success message
    // await waitFor(() => {
    //   expect(screen.getByText(/application created successfully/i)).toBeInTheDocument();
    // });
  }

  /**
   * Test deployment flow
   */
  static async testDeploymentFlow() {
    // Implementation would test the full deployment process
    // from triggering a deployment to monitoring its progress
  }

  /**
   * Test real-time updates
   */
  static async testRealTimeUpdates() {
    // Test WebSocket connections and real-time data updates
  }
}
