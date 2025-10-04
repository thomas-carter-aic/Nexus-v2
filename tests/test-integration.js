#!/usr/bin/env node

/**
 * Integration Test Runner
 * 
 * Comprehensive testing script to verify frontend-backend integration
 */

const { spawn, exec } = require('child_process');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

class IntegrationTestRunner {
  constructor() {
    this.backendUrl = 'http://localhost:8000';
    this.frontendUrl = 'http://localhost:3000';
    this.backendProcess = null;
    this.frontendProcess = null;
    this.testResults = {
      backend: {},
      frontend: {},
      integration: {},
      e2e: {},
    };
  }

  async run() {
    console.log('🚀 Starting Ultimate PaaS Integration Tests\n');
    
    try {
      // Step 1: Check prerequisites
      await this.checkPrerequisites();
      
      // Step 2: Start backend
      await this.startBackend();
      
      // Step 3: Start frontend
      await this.startFrontend();
      
      // Step 4: Run API integration tests
      await this.runApiTests();
      
      // Step 5: Run frontend tests
      await this.runFrontendTests();
      
      // Step 6: Run E2E tests
      await this.runE2ETests();
      
      // Step 7: Generate report
      this.generateReport();
      
    } catch (error) {
      console.error('❌ Integration tests failed:', error.message);
      process.exit(1);
    } finally {
      await this.cleanup();
    }
  }

  async checkPrerequisites() {
    console.log('📋 Checking prerequisites...');
    
    // Check if backend directory exists
    const backendPath = path.join(__dirname, '..', 'ultimate-paas-base');
    if (!fs.existsSync(backendPath)) {
      throw new Error('Backend directory not found. Please ensure ultimate-paas-base exists in parent directory.');
    }
    
    // Check if backend has requirements.txt
    const requirementsPath = path.join(backendPath, 'requirements.txt');
    if (!fs.existsSync(requirementsPath)) {
      throw new Error('Backend requirements.txt not found. Please ensure backend is properly set up.');
    }
    
    // Check if frontend dependencies are installed
    if (!fs.existsSync(path.join(__dirname, 'node_modules'))) {
      console.log('📦 Installing frontend dependencies...');
      await this.execCommand('npm install');
    }
    
    console.log('✅ Prerequisites check passed\n');
  }

  async startBackend() {
    console.log('🐍 Starting backend server...');
    
    const backendPath = path.join(__dirname, '..', 'ultimate-paas-base');
    
    return new Promise((resolve, reject) => {
      // Start backend process
      this.backendProcess = spawn('python', ['src/main.py'], {
        cwd: backendPath,
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      let output = '';
      this.backendProcess.stdout.on('data', (data) => {
        output += data.toString();
        if (output.includes('Uvicorn running on')) {
          console.log('✅ Backend server started\n');
          resolve();
        }
      });

      this.backendProcess.stderr.on('data', (data) => {
        console.error('Backend error:', data.toString());
      });

      this.backendProcess.on('error', (error) => {
        reject(new Error(`Failed to start backend: ${error.message}`));
      });

      // Timeout after 30 seconds
      setTimeout(() => {
        if (!output.includes('Uvicorn running on')) {
          reject(new Error('Backend failed to start within 30 seconds'));
        }
      }, 30000);
    });
  }

  async startFrontend() {
    console.log('⚛️  Starting frontend servers...');
    
    return new Promise((resolve, reject) => {
      // Start all microfrontends
      this.frontendProcess = spawn('npm', ['run', 'dev'], {
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      let output = '';
      this.frontendProcess.stdout.on('data', (data) => {
        output += data.toString();
        // Check if all servers are ready
        if (output.includes('Ready in') && output.includes('3000')) {
          console.log('✅ Frontend servers started\n');
          resolve();
        }
      });

      this.frontendProcess.stderr.on('data', (data) => {
        console.error('Frontend error:', data.toString());
      });

      this.frontendProcess.on('error', (error) => {
        reject(new Error(`Failed to start frontend: ${error.message}`));
      });

      // Timeout after 60 seconds
      setTimeout(() => {
        if (!output.includes('Ready in')) {
          reject(new Error('Frontend failed to start within 60 seconds'));
        }
      }, 60000);
    });
  }

  async runApiTests() {
    console.log('🧪 Running API integration tests...');
    
    try {
      // Import and run the API tester
      const { BackendApiTester } = require('./packages/testing/src/api-testing');
      const tester = new BackendApiTester(this.backendUrl);
      
      this.testResults.integration = await tester.runFullIntegrationTest();
      
      if (this.testResults.integration.success) {
        console.log('✅ API integration tests passed\n');
      } else {
        console.log('⚠️  Some API integration tests failed\n');
      }
    } catch (error) {
      console.error('❌ API integration tests failed:', error.message);
      this.testResults.integration = { success: false, error: error.message };
    }
  }

  async runFrontendTests() {
    console.log('🧪 Running frontend unit tests...');
    
    try {
      await this.execCommand('npm run test -- --watchAll=false');
      this.testResults.frontend.success = true;
      console.log('✅ Frontend tests passed\n');
    } catch (error) {
      console.log('⚠️  Some frontend tests failed\n');
      this.testResults.frontend = { success: false, error: error.message };
    }
  }

  async runE2ETests() {
    console.log('🎭 Running E2E tests...');
    
    try {
      // Wait for services to be fully ready
      await this.waitForServices();
      
      await this.execCommand('npx playwright test');
      this.testResults.e2e.success = true;
      console.log('✅ E2E tests passed\n');
    } catch (error) {
      console.log('⚠️  Some E2E tests failed\n');
      this.testResults.e2e = { success: false, error: error.message };
    }
  }

  async waitForServices() {
    console.log('⏳ Waiting for services to be ready...');
    
    // Wait for backend
    await this.waitForUrl(this.backendUrl + '/health');
    
    // Wait for frontend
    await this.waitForUrl(this.frontendUrl);
    
    console.log('✅ All services are ready\n');
  }

  async waitForUrl(url, timeout = 30000) {
    const start = Date.now();
    
    while (Date.now() - start < timeout) {
      try {
        await axios.get(url, { timeout: 5000 });
        return;
      } catch (error) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    throw new Error(`Service at ${url} not ready within ${timeout}ms`);
  }

  generateReport() {
    console.log('📊 Test Results Summary');
    console.log('========================\n');
    
    const results = [
      { name: 'API Integration', result: this.testResults.integration },
      { name: 'Frontend Tests', result: this.testResults.frontend },
      { name: 'E2E Tests', result: this.testResults.e2e },
    ];
    
    results.forEach(({ name, result }) => {
      const status = result.success ? '✅ PASS' : '❌ FAIL';
      console.log(`${name}: ${status}`);
      if (!result.success && result.error) {
        console.log(`  Error: ${result.error}`);
      }
    });
    
    console.log('\n');
    
    const overallSuccess = results.every(r => r.result.success);
    
    if (overallSuccess) {
      console.log('🎉 All integration tests passed!');
      console.log('✅ Frontend is ready for production deployment.');
    } else {
      console.log('⚠️  Some tests failed. Please review the results above.');
      console.log('🔧 Fix the issues before deploying to production.');
    }
    
    // Save detailed report
    const reportPath = path.join(__dirname, 'integration-test-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.testResults, null, 2));
    console.log(`\n📄 Detailed report saved to: ${reportPath}`);
  }

  async cleanup() {
    console.log('\n🧹 Cleaning up...');
    
    if (this.backendProcess) {
      this.backendProcess.kill();
    }
    
    if (this.frontendProcess) {
      this.frontendProcess.kill();
    }
    
    console.log('✅ Cleanup complete');
  }

  execCommand(command) {
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          reject(error);
        } else {
          resolve(stdout);
        }
      });
    });
  }
}

// Run the tests if this script is executed directly
if (require.main === module) {
  const runner = new IntegrationTestRunner();
  runner.run().catch(console.error);
}

module.exports = IntegrationTestRunner;
