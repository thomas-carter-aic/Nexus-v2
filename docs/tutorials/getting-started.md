# Getting Started with AI-Native PaaS Platform

This comprehensive tutorial will guide you through deploying your first AI-driven application, setting up monitoring, and leveraging the platform's intelligent features.

## Prerequisites

Before starting, ensure you have:
- AWS account with appropriate permissions
- Python 3.9+ installed
- Docker installed and running
- Node.js 14+ (for AWS CDK)
- Git installed

## Tutorial 1: Deploying Your First AI-Driven Application

### Step 1: Platform Setup

1. **Clone and setup the platform**
   ```bash
   git clone https://github.com/your-org/ai-native-paas.git
   cd ai-native-paas
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Configure AWS credentials**
   ```bash
   aws configure
   # AWS Access Key ID: [Your Access Key]
   # AWS Secret Access Key: [Your Secret Key]
   # Default region name: us-east-1
   # Default output format: json
   ```

3. **Deploy infrastructure**
   ```bash
   cd deployments/aws-cdk
   npm install
   cdk bootstrap
   cdk deploy PaaSPlatformStack --require-approval never
   ```

   **Expected Output:**
   ```
   ✅  PaaSPlatformStack
   
   Outputs:
   PaaSPlatformStack.APIGatewayURL = https://abc123.execute-api.us-east-1.amazonaws.com/prod
   PaaSPlatformStack.ClusterName = paas-cluster
   PaaSPlatformStack.EventStoreTable = paas-event-store
   ```

### Step 2: Create Your First Application

1. **Initialize the CLI**
   ```bash
   cd ../../
   export PAAS_API_URL=https://abc123.execute-api.us-east-1.amazonaws.com/prod
   python -m src.cli.main configure --api-url $PAAS_API_URL
   ```

2. **Create a sample web application**
   ```bash
   # Create application configuration
   cat > my-app-config.yaml << EOF
   name: "my-first-app"
   description: "My first AI-native application"
   image: "nginx:latest"
   port: 80
   resources:
     cpu: 0.5
     memory: 512
     storage: 10
   scaling:
     strategy: "predictive"
     min_instances: 1
     max_instances: 5
     target_cpu: 70
   environment:
     - name: "APP_ENV"
       value: "production"
     - name: "LOG_LEVEL"
       value: "INFO"
   EOF
   ```

3. **Deploy the application**
   ```bash
   python -m src.cli.main app create --config my-app-config.yaml
   ```

   **Expected Output:**
   ```
   ✅ Application created successfully
   Application ID: app-12345678-1234-1234-1234-123456789012
   Status: PENDING
   
   🤖 AI Analysis:
   - Deployment risk: LOW (confidence: 92%)
   - Estimated deployment time: 3-5 minutes
   - Recommended instance type: t3.small
   - Cost estimate: $0.02/hour
   ```

4. **Monitor deployment progress**
   ```bash
   python -m src.cli.main app status my-first-app --follow
   ```

   **Expected Output:**
   ```
   📊 Deployment Progress:
   [████████████████████████████████████████] 100%
   
   Status: RUNNING
   Instances: 1/1 healthy
   URL: https://my-first-app.paas-platform.com
   
   🤖 AI Insights:
   - Deployment completed in 4m 23s
   - All health checks passed
   - Performance baseline established
   - Auto-scaling enabled and learning
   ```

### Step 3: Verify Deployment

1. **Check application health**
   ```bash
   curl https://my-first-app.paas-platform.com/health
   ```

   **Expected Response:**
   ```json
   {
     "status": "healthy",
     "version": "1.0.0",
     "timestamp": "2024-01-15T10:30:00Z",
     "checks": {
       "database": "healthy",
       "cache": "healthy",
       "external_apis": "healthy"
     }
   }
   ```

2. **View application logs**
   ```bash
   python -m src.cli.main app logs my-first-app --tail 50
   ```

   **Expected Output:**
   ```
   2024-01-15 10:30:00 [INFO] Application started successfully
   2024-01-15 10:30:01 [INFO] Health check endpoint registered
   2024-01-15 10:30:02 [INFO] AI monitoring enabled
   2024-01-15 10:30:03 [INFO] Ready to serve traffic
   ```

## Tutorial 2: Setting Up AI-Driven Auto-Scaling

### Step 1: Configure Predictive Scaling

1. **Update scaling configuration**
   ```bash
   cat > scaling-config.yaml << EOF
   strategy: "predictive"
   min_instances: 1
   max_instances: 10
   target_metrics:
     cpu_utilization: 70
     memory_utilization: 80
     response_time: 200
   ai_settings:
     prediction_horizon: 60  # minutes
     confidence_threshold: 0.8
     learning_rate: 0.1
   custom_metrics:
     - name: "business_transactions_per_minute"
       target: 1000
       weight: 0.3
   EOF
   
   python -m src.cli.main app update-scaling my-first-app --config scaling-config.yaml
   ```

   **Expected Output:**
   ```
   ✅ Scaling configuration updated
   
   🤖 AI Analysis:
   - Configuration validated
   - Historical data: 7 days available
   - Model accuracy: 94.2%
   - Next prediction: 2024-01-15T11:00:00Z
   
   📊 Scaling Insights:
   - Peak traffic predicted: 15:00-17:00 daily
   - Recommended scale-up: +2 instances at 14:45
   - Cost optimization: 23% savings vs reactive scaling
   ```

### Step 2: Monitor AI Scaling Decisions

1. **View scaling events**
   ```bash
   python -m src.cli.main app scaling-events my-first-app --last 24h
   ```

   **Expected Output:**
   ```
   📈 Scaling Events (Last 24 hours):
   
   2024-01-15 09:45:00 | SCALE_UP   | 1 → 2 instances
   Reason: AI predicted traffic increase (confidence: 87%)
   Actual traffic increase: +45% (prediction accurate)
   
   2024-01-15 14:30:00 | SCALE_UP   | 2 → 4 instances  
   Reason: High CPU utilization + predicted peak (confidence: 92%)
   Cost impact: +$0.04/hour, Performance improvement: 35%
   
   2024-01-15 18:15:00 | SCALE_DOWN | 4 → 2 instances
   Reason: Traffic decline predicted (confidence: 89%)
   Cost savings: $0.02/hour
   ```

2. **View AI model performance**
   ```bash
   python -m src.cli.main ai model-stats --application my-first-app
   ```

   **Expected Output:**
   ```
   🤖 AI Model Performance:
   
   Scaling Predictor:
   - Accuracy: 94.2%
   - Precision: 91.8%
   - Recall: 96.1%
   - Last updated: 2024-01-15T08:00:00Z
   
   Anomaly Detector:
   - Sensitivity: 95.5%
   - False positive rate: 2.1%
   - Detection latency: 1.3 minutes
   
   Cost Optimizer:
   - Savings achieved: 28.5%
   - Recommendations accepted: 87%
   - ROI: 340%
   ```

## Tutorial 3: Building and Deploying a Custom Plugin

### Step 1: Create Plugin Structure

1. **Generate plugin template**
   ```bash
   python -m src.cli.main plugin create \
     --name "custom-monitoring" \
     --type "monitoring" \
     --description "Custom business metrics monitoring"
   ```

   **Generated Structure:**
   ```
   plugins/custom-monitoring/
   ├── plugin.yaml
   ├── src/
   │   ├── __init__.py
   │   └── main.py
   ├── tests/
   │   └── test_plugin.py
   └── README.md
   ```

2. **Implement plugin logic**
   ```python
   # plugins/custom-monitoring/src/main.py
   from paas.plugin import PluginBase, MetricCollector
   import requests
   import time
   
   class CustomMonitoringPlugin(PluginBase):
       """Custom monitoring plugin for business metrics"""
       
       def initialize(self):
           """Initialize plugin with configuration"""
           self.api_endpoint = self.config.get('api_endpoint')
           self.collection_interval = self.config.get('interval', 60)
           self.metrics_collector = MetricCollector(self.context)
           
       def execute(self, context):
           """Main plugin execution logic"""
           try:
               # Collect business metrics from external API
               business_data = self._fetch_business_metrics()
               
               # Publish metrics to platform
               self._publish_metrics(business_data)
               
               # Analyze trends
               trend_analysis = self._analyze_trends(business_data)
               
               return {
                   "status": "success",
                   "metrics_collected": len(business_data),
                   "trends": trend_analysis,
                   "timestamp": time.time()
               }
               
           except Exception as e:
               self.logger.error(f"Plugin execution failed: {str(e)}")
               return {"status": "error", "message": str(e)}
       
       def _fetch_business_metrics(self):
           """Fetch business metrics from external API"""
           response = requests.get(f"{self.api_endpoint}/metrics")
           response.raise_for_status()
           return response.json()
       
       def _publish_metrics(self, data):
           """Publish metrics to platform monitoring system"""
           for metric_name, value in data.items():
               self.metrics_collector.publish_metric(
                   name=f"business.{metric_name}",
                   value=value,
                   dimensions={
                       "application_id": self.context.application_id,
                       "plugin": "custom-monitoring"
                   }
               )
       
       def _analyze_trends(self, data):
           """Analyze metric trends"""
           # Simple trend analysis
           return {
               "revenue_trend": "increasing" if data.get("revenue", 0) > 1000 else "stable",
               "user_growth": "positive" if data.get("active_users", 0) > 500 else "neutral"
           }
   ```

3. **Configure plugin**
   ```yaml
   # plugins/custom-monitoring/plugin.yaml
   name: "custom-monitoring"
   version: "1.0.0"
   description: "Custom business metrics monitoring plugin"
   author: "Your Name"
   
   runtime:
     python_version: "3.9"
     memory_limit: "128MB"
     timeout: "30s"
   
   permissions:
     - "metrics:publish"
     - "http:external"
   
   configuration:
     api_endpoint:
       type: "string"
       required: true
       description: "Business metrics API endpoint"
     interval:
       type: "integer"
       default: 60
       description: "Collection interval in seconds"
   
   schedule:
     type: "interval"
     interval: "60s"
   ```

### Step 2: Test and Deploy Plugin

1. **Test plugin locally**
   ```bash
   cd plugins/custom-monitoring
   python -m pytest tests/ -v
   ```

   **Expected Output:**
   ```
   ===== test session starts =====
   
   tests/test_plugin.py::test_plugin_initialization PASSED
   tests/test_plugin.py::test_metric_collection PASSED  
   tests/test_plugin.py::test_error_handling PASSED
   tests/test_plugin.py::test_trend_analysis PASSED
   
   ===== 4 passed in 2.34s =====
   ```

2. **Deploy plugin**
   ```bash
   cd ../../
   python -m src.cli.main plugin deploy custom-monitoring \
     --config '{"api_endpoint": "https://api.mybusiness.com"}'
   ```

   **Expected Output:**
   ```
   🔌 Deploying plugin: custom-monitoring
   
   ✅ Plugin validation passed
   ✅ Security scan completed
   ✅ Resource allocation: 128MB memory, 30s timeout
   ✅ Plugin deployed successfully
   
   Plugin ID: plugin-87654321-4321-4321-4321-210987654321
   Status: ACTIVE
   Next execution: 2024-01-15T10:31:00Z
   ```

3. **Monitor plugin execution**
   ```bash
   python -m src.cli.main plugin logs custom-monitoring --tail 20
   ```

   **Expected Output:**
   ```
   2024-01-15 10:31:00 [INFO] Plugin execution started
   2024-01-15 10:31:01 [INFO] Fetching metrics from https://api.mybusiness.com
   2024-01-15 10:31:02 [INFO] Collected 5 business metrics
   2024-01-15 10:31:02 [INFO] Published metrics to platform
   2024-01-15 10:31:03 [INFO] Trend analysis: revenue_trend=increasing
   2024-01-15 10:31:03 [INFO] Plugin execution completed successfully
   ```

## Tutorial 4: Setting Up CI/CD with AI Optimization

### Step 1: Configure Repository

1. **Create application repository**
   ```bash
   # Initialize new repository for your application
   mkdir my-paas-app && cd my-paas-app
   git init
   
   # Create application structure
   mkdir -p src tests deployments
   
   # Create sample application
   cat > src/app.py << EOF
   from flask import Flask, jsonify
   import os
   
   app = Flask(__name__)
   
   @app.route('/health')
   def health():
       return jsonify({
           "status": "healthy",
           "version": os.getenv("APP_VERSION", "1.0.0")
       })
   
   @app.route('/')
   def hello():
       return jsonify({
           "message": "Hello from AI-Native PaaS!",
           "features": ["AI Scaling", "Smart Monitoring", "Auto Deployment"]
       })
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)
   EOF
   ```

2. **Create Dockerfile**
   ```dockerfile
   # Dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY src/ ./src/
   EXPOSE 8080
   
   CMD ["python", "src/app.py"]
   ```

3. **Create requirements.txt**
   ```txt
   Flask==2.3.3
   gunicorn==21.2.0
   ```

### Step 2: Set Up CI/CD Pipeline

1. **Create buildspec.yml**
   ```yaml
   # buildspec.yml
   version: 0.2
   
   phases:
     pre_build:
       commands:
         - echo Logging in to Amazon ECR...
         - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
         - echo Getting AI test prioritization...
         - python /opt/paas/scripts/prioritize_tests.py --output test_plan.json
     
     build:
       commands:
         - echo Build started on `date`
         - echo Running AI-prioritized tests...
         - pytest tests/ --json-report --json-report-file=test_results.json
         - echo Building the Docker image...
         - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
         - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
     
     post_build:
       commands:
         - echo Build completed on `date`
         - echo Pushing the Docker image...
         - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
         - echo Getting AI deployment risk assessment...
         - python /opt/paas/scripts/assess_deployment_risk.py --image $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
   
   artifacts:
     files:
       - '**/*'
   ```

2. **Create deployment configuration**
   ```yaml
   # deployments/paas-config.yaml
   application:
     name: "my-paas-app"
     version: "${BUILD_NUMBER}"
   
   deployment:
     strategy: "blue_green"
     ai_optimization: true
     health_check:
       path: "/health"
       timeout: 30
       interval: 10
     
   scaling:
     strategy: "predictive"
     ai_learning: true
     min_instances: 2
     max_instances: 20
   
   monitoring:
     ai_anomaly_detection: true
     custom_metrics:
       - name: "business_transactions"
         path: "/metrics/transactions"
       - name: "user_satisfaction"
         path: "/metrics/satisfaction"
   ```

### Step 3: Deploy with AI Optimization

1. **Trigger deployment**
   ```bash
   # Commit and push code
   git add .
   git commit -m "Initial application with AI-native PaaS integration"
   git push origin main
   ```

   **Expected CI/CD Output:**
   ```
   🤖 AI Pipeline Analysis:
   
   Test Prioritization:
   - High priority: 12 tests (estimated 3m 45s)
   - Medium priority: 8 tests (estimated 2m 30s)  
   - Low priority: 15 tests (skipped for fast feedback)
   - Time saved: 67% (8m 15s → 2m 45s)
   
   Risk Assessment:
   - Deployment risk: LOW (confidence: 94%)
   - Code complexity: MEDIUM
   - Test coverage: 89%
   - Dependency changes: 2 (low risk)
   - Recommended strategy: Blue/Green
   
   Deployment Optimization:
   - Optimal deployment time: Now (low traffic period)
   - Instance type recommendation: t3.medium
   - Expected performance improvement: 15%
   - Cost impact: +$0.03/hour (+12%)
   ```

2. **Monitor deployment progress**
   ```bash
   python -m src.cli.main deployment status --follow
   ```

   **Expected Output:**
   ```
   🚀 Blue/Green Deployment Progress:
   
   Phase 1: Green Environment Setup     [████████████████████] 100%
   Phase 2: Health Checks              [████████████████████] 100%
   Phase 3: Traffic Switch (0% → 100%) [████████████████████] 100%
   Phase 4: Stability Monitoring       [████████████████████] 100%
   Phase 5: Blue Environment Cleanup   [████████████████████] 100%
   
   ✅ Deployment completed successfully in 4m 32s
   
   🤖 AI Analysis:
   - Deployment risk prediction: ACCURATE (actual: no issues)
   - Performance improvement: 18% (vs predicted 15%)
   - Zero downtime achieved
   - Auto-scaling learning initiated
   
   📊 Post-Deployment Metrics:
   - Response time: 145ms (improved from 178ms)
   - Error rate: 0.02% (within SLA)
   - User satisfaction: 4.7/5.0
   ```

## Tutorial 5: Advanced Monitoring and AI Insights

### Step 1: Set Up Custom Dashboards

1. **Create AI-enhanced dashboard**
   ```bash
   python -m src.cli.main dashboard create \
     --name "my-app-ai-dashboard" \
     --application my-first-app \
     --ai-insights enabled
   ```

   **Dashboard Features Created:**
   ```
   📊 AI-Enhanced Dashboard Created:
   
   Widgets Added:
   - Real-time performance metrics with AI predictions
   - Anomaly detection alerts with confidence scores
   - User behavior analysis with business impact
   - Cost optimization recommendations
   - Predictive scaling timeline
   - Business KPI correlation matrix
   
   Dashboard URL: https://console.aws.amazon.com/cloudwatch/home#dashboards:name=my-app-ai-dashboard
   ```

2. **Configure custom alerts**
   ```bash
   # Create intelligent alert that learns from false positives
   python -m src.cli.main alerts create \
     --name "smart-performance-alert" \
     --metric "ResponseTime" \
     --ai-threshold dynamic \
     --learning-enabled true \
     --notification slack://alerts-channel
   ```

   **Expected Output:**
   ```
   🚨 Smart Alert Created:
   
   Alert: smart-performance-alert
   - AI-driven threshold: 250ms (learned from 30 days of data)
   - Confidence requirement: 85%
   - False positive rate: 1.2% (improving over time)
   - Learning enabled: Threshold adapts to usage patterns
   
   Notification channels:
   - Slack: #alerts-channel
   - Email: ops-team@company.com (escalation after 5 minutes)
   ```

### Step 2: Analyze AI Insights

1. **Generate comprehensive insights report**
   ```bash
   python -m src.cli.main insights generate \
     --application my-first-app \
     --period 7d \
     --include-predictions true
   ```

   **Sample Report Output:**
   ```
   📈 AI Insights Report (7 days)
   
   Executive Summary:
   - Application health: EXCELLENT (98.5% uptime)
   - Performance trend: IMPROVING (+12% response time)
   - Cost efficiency: OPTIMIZED (31% savings vs baseline)
   - User satisfaction: HIGH (4.6/5.0 rating)
   
   🤖 AI Predictions (Next 7 days):
   - Traffic increase expected: +25% (Thu-Fri)
   - Scaling recommendation: +2 instances on Thursday 2PM
   - Potential cost savings: $45/week with spot instances
   - Anomaly risk: LOW (2.1% probability)
   
   💡 Optimization Opportunities:
   1. Database query optimization (15% performance gain)
   2. CDN configuration update (8% faster load times)
   3. Memory allocation tuning (12% cost reduction)
   
   📊 Business Impact:
   - Revenue correlation: +$1,200 per 100ms response time improvement
   - User retention: 94% (above industry average of 87%)
   - Feature adoption: API v2 usage growing 23% week-over-week
   ```

2. **View AI model learning progress**
   ```bash
   python -m src.cli.main ai learning-stats --application my-first-app
   ```

   **Expected Output:**
   ```
   🧠 AI Learning Progress:
   
   Scaling Predictor Model:
   - Training data: 168 hours of metrics
   - Accuracy improvement: 87% → 94% (over 7 days)
   - Next retraining: 2024-01-22T08:00:00Z
   - Confidence trend: INCREASING
   
   Anomaly Detection Model:
   - Baseline established: ✅
   - False positive reduction: 45% (week-over-week)
   - New pattern recognition: 3 patterns learned
   - Sensitivity: Auto-tuned to 95.2%
   
   Cost Optimization Model:
   - Savings achieved: $127.50 (this week)
   - Recommendation acceptance rate: 89%
   - ROI: 340% (cost of AI vs savings)
   - Next optimization cycle: 2024-01-16T00:00:00Z
   ```

## Troubleshooting Common Issues

### Issue 1: Deployment Fails with AI Risk Assessment

**Problem:** Deployment blocked due to high AI-assessed risk

**Solution:**
```bash
# Check risk factors
python -m src.cli.main deployment risk-analysis my-first-app

# Override with manual approval (if appropriate)
python -m src.cli.main deployment approve <deployment-id> \
  --override-risk true \
  --reason "Manual review completed"

# Or address specific risk factors
python -m src.cli.main deployment optimize <deployment-id>
```

### Issue 2: AI Scaling Not Working

**Problem:** Predictive scaling not triggering

**Solution:**
```bash
# Check AI model status
python -m src.cli.main ai model-health --application my-first-app

# Verify training data
python -m src.cli.main ai training-data --application my-first-app

# Fallback to reactive scaling temporarily
python -m src.cli.main app update-scaling my-first-app \
  --strategy reactive --temporary true
```

### Issue 3: Plugin Execution Failures

**Problem:** Custom plugin failing to execute

**Solution:**
```bash
# Check plugin logs
python -m src.cli.main plugin logs custom-monitoring --errors-only

# Validate plugin configuration
python -m src.cli.main plugin validate custom-monitoring

# Test plugin in sandbox
python -m src.cli.main plugin test custom-monitoring --sandbox true
```

## Next Steps

Congratulations! You've successfully:
- ✅ Deployed your first AI-driven application
- ✅ Configured predictive auto-scaling
- ✅ Built and deployed a custom plugin
- ✅ Set up AI-optimized CI/CD pipeline
- ✅ Created intelligent monitoring and dashboards

### Advanced Topics to Explore

1. **Multi-Region Deployment**
   - Global traffic routing
   - Data residency compliance
   - Disaster recovery automation

2. **Advanced AI Features**
   - Custom ML model integration
   - Business metric correlation
   - Predictive cost optimization

3. **Enterprise Integration**
   - SSO and advanced RBAC
   - Compliance automation
   - Custom plugin marketplace

4. **Performance Optimization**
   - Advanced caching strategies
   - Database optimization
   - CDN configuration

### Resources

- [API Documentation](../api/README.md)
- [Plugin Development Guide](../plugins/README.md)
- [Architecture Deep Dive](../architecture/README.md)
- [Best Practices](../best-practices/README.md)

---

**Need Help?** Join our [community forum](https://community.paas-platform.com) or [Slack channel](https://slack.paas-platform.com) for support and discussions.
