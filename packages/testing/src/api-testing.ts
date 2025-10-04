import axios, { AxiosInstance } from 'axios';
import { Application, User, Deployment, ApiResponse } from '@ultimate-paas/types';

/**
 * API Testing Utilities for Backend Integration
 * 
 * This module provides utilities to test the integration between
 * the frontend and the ultimate-paas-base backend.
 */

export class BackendApiTester {
  private client: AxiosInstance;
  private baseUrl: string;
  private authToken?: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth interceptor
    this.client.interceptors.request.use((config) => {
      if (this.authToken) {
        config.headers.Authorization = `Bearer ${this.authToken}`;
      }
      return config;
    });
  }

  /**
   * Test backend connectivity
   */
  async testConnectivity(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.status === 200;
    } catch (error) {
      console.error('Backend connectivity test failed:', error);
      return false;
    }
  }

  /**
   * Test authentication endpoints
   */
  async testAuthentication(credentials: { username: string; password: string }): Promise<{
    success: boolean;
    token?: string;
    error?: string;
  }> {
    try {
      const response = await this.client.post('/auth/login', credentials);
      
      if (response.data.access_token) {
        this.authToken = response.data.access_token;
        return {
          success: true,
          token: response.data.access_token,
        };
      }
      
      return {
        success: false,
        error: 'No token received',
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || error.message,
      };
    }
  }

  /**
   * Test application management endpoints
   */
  async testApplicationEndpoints(): Promise<{
    success: boolean;
    results: Record<string, boolean>;
    errors: string[];
  }> {
    const results: Record<string, boolean> = {};
    const errors: string[] = [];

    try {
      // Test GET /applications
      const listResponse = await this.client.get('/api/v1/applications');
      results.listApplications = listResponse.status === 200;
    } catch (error: any) {
      results.listApplications = false;
      errors.push(`List applications failed: ${error.message}`);
    }

    try {
      // Test POST /applications
      const createData = {
        name: 'test-app',
        description: 'Test application for integration testing',
        repository: {
          url: 'https://github.com/test/test-app',
          branch: 'main',
          provider: 'github',
        },
      };
      
      const createResponse = await this.client.post('/api/v1/applications', createData);
      results.createApplication = createResponse.status === 201;
      
      if (createResponse.data.data?.id) {
        const appId = createResponse.data.data.id;
        
        // Test GET /applications/:id
        try {
          const getResponse = await this.client.get(`/api/v1/applications/${appId}`);
          results.getApplication = getResponse.status === 200;
        } catch (error: any) {
          results.getApplication = false;
          errors.push(`Get application failed: ${error.message}`);
        }

        // Test PUT /applications/:id
        try {
          const updateData = { description: 'Updated description' };
          const updateResponse = await this.client.put(`/api/v1/applications/${appId}`, updateData);
          results.updateApplication = updateResponse.status === 200;
        } catch (error: any) {
          results.updateApplication = false;
          errors.push(`Update application failed: ${error.message}`);
        }

        // Test DELETE /applications/:id
        try {
          const deleteResponse = await this.client.delete(`/api/v1/applications/${appId}`);
          results.deleteApplication = deleteResponse.status === 200;
        } catch (error: any) {
          results.deleteApplication = false;
          errors.push(`Delete application failed: ${error.message}`);
        }
      }
    } catch (error: any) {
      results.createApplication = false;
      errors.push(`Create application failed: ${error.message}`);
    }

    return {
      success: Object.values(results).every(Boolean),
      results,
      errors,
    };
  }

  /**
   * Test deployment endpoints
   */
  async testDeploymentEndpoints(): Promise<{
    success: boolean;
    results: Record<string, boolean>;
    errors: string[];
  }> {
    const results: Record<string, boolean> = {};
    const errors: string[] = [];

    try {
      // Test GET /deployments
      const listResponse = await this.client.get('/api/v1/deployments');
      results.listDeployments = listResponse.status === 200;
    } catch (error: any) {
      results.listDeployments = false;
      errors.push(`List deployments failed: ${error.message}`);
    }

    return {
      success: Object.values(results).every(Boolean),
      results,
      errors,
    };
  }

  /**
   * Test AI/Analytics endpoints
   */
  async testAIEndpoints(): Promise<{
    success: boolean;
    results: Record<string, boolean>;
    errors: string[];
  }> {
    const results: Record<string, boolean> = {};
    const errors: string[] = [];

    try {
      // Test GET /ai/insights
      const insightsResponse = await this.client.get('/api/v1/ai/insights');
      results.getInsights = insightsResponse.status === 200;
    } catch (error: any) {
      results.getInsights = false;
      errors.push(`Get AI insights failed: ${error.message}`);
    }

    try {
      // Test GET /ai/recommendations
      const recommendationsResponse = await this.client.get('/api/v1/ai/recommendations');
      results.getRecommendations = recommendationsResponse.status === 200;
    } catch (error: any) {
      results.getRecommendations = false;
      errors.push(`Get AI recommendations failed: ${error.message}`);
    }

    return {
      success: Object.values(results).every(Boolean),
      results,
      errors,
    };
  }

  /**
   * Test GraphQL endpoint
   */
  async testGraphQLEndpoint(): Promise<{
    success: boolean;
    error?: string;
  }> {
    try {
      const query = `
        query {
          applications {
            id
            name
            status
          }
        }
      `;

      const response = await this.client.post('/graphql', { query });
      
      return {
        success: response.status === 200 && !response.data.errors,
        error: response.data.errors?.[0]?.message,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Run comprehensive backend integration tests
   */
  async runFullIntegrationTest(): Promise<{
    success: boolean;
    results: Record<string, any>;
    summary: string;
  }> {
    const results: Record<string, any> = {};
    
    console.log('🧪 Starting Backend Integration Tests...\n');

    // Test 1: Connectivity
    console.log('1. Testing backend connectivity...');
    results.connectivity = await this.testConnectivity();
    console.log(`   ${results.connectivity ? '✅' : '❌'} Connectivity: ${results.connectivity ? 'PASS' : 'FAIL'}\n`);

    if (!results.connectivity) {
      return {
        success: false,
        results,
        summary: 'Backend is not accessible. Please ensure ultimate-paas-base is running.',
      };
    }

    // Test 2: Authentication
    console.log('2. Testing authentication...');
    results.authentication = await this.testAuthentication({
      username: 'admin',
      password: 'admin123', // Default test credentials
    });
    console.log(`   ${results.authentication.success ? '✅' : '❌'} Authentication: ${results.authentication.success ? 'PASS' : 'FAIL'}`);
    if (!results.authentication.success) {
      console.log(`   Error: ${results.authentication.error}\n`);
    } else {
      console.log('   Token received successfully\n');
    }

    // Test 3: Application endpoints
    console.log('3. Testing application management endpoints...');
    results.applications = await this.testApplicationEndpoints();
    console.log(`   ${results.applications.success ? '✅' : '❌'} Applications: ${results.applications.success ? 'PASS' : 'FAIL'}`);
    Object.entries(results.applications.results).forEach(([test, passed]) => {
      console.log(`     ${passed ? '✅' : '❌'} ${test}: ${passed ? 'PASS' : 'FAIL'}`);
    });
    if (results.applications.errors.length > 0) {
      results.applications.errors.forEach(error => console.log(`     Error: ${error}`));
    }
    console.log('');

    // Test 4: Deployment endpoints
    console.log('4. Testing deployment endpoints...');
    results.deployments = await this.testDeploymentEndpoints();
    console.log(`   ${results.deployments.success ? '✅' : '❌'} Deployments: ${results.deployments.success ? 'PASS' : 'FAIL'}\n`);

    // Test 5: AI endpoints
    console.log('5. Testing AI/Analytics endpoints...');
    results.ai = await this.testAIEndpoints();
    console.log(`   ${results.ai.success ? '✅' : '❌'} AI/Analytics: ${results.ai.success ? 'PASS' : 'FAIL'}\n`);

    // Test 6: GraphQL
    console.log('6. Testing GraphQL endpoint...');
    results.graphql = await this.testGraphQLEndpoint();
    console.log(`   ${results.graphql.success ? '✅' : '❌'} GraphQL: ${results.graphql.success ? 'PASS' : 'FAIL'}`);
    if (!results.graphql.success && results.graphql.error) {
      console.log(`   Error: ${results.graphql.error}`);
    }
    console.log('');

    const overallSuccess = results.connectivity && 
                          results.authentication.success && 
                          results.applications.success && 
                          results.deployments.success;

    const summary = overallSuccess 
      ? '🎉 All integration tests passed! Frontend is ready to connect to backend.'
      : '⚠️  Some integration tests failed. Please check the backend configuration.';

    console.log(summary);

    return {
      success: overallSuccess,
      results,
      summary,
    };
  }
}
