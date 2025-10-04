import { DocArticle } from '@/types/docs'

export const gettingStartedArticles: DocArticle[] = [
  {
    id: 'platform-overview',
    title: 'Platform Overview',
    description: 'Introduction to the Applied Innovations Nexus platform and its capabilities',
    slug: 'platform-overview',
    sectionId: 'getting-started',
    order: 1,
    difficulty: 'beginner',
    tags: ['overview', 'introduction', 'platform'],
    lastUpdated: '2024-07-04',
    readTime: 5,
    content: `
# Platform Overview

Welcome to the Applied Innovations Nexus platform - your comprehensive solution for AI transformation and automation.

## What is Nexus?

Nexus is an enterprise-grade AI platform that enables organizations to:

- **Deploy AI Agents**: Create and manage intelligent agents for various business processes
- **Automate Workflows**: Build sophisticated automation pipelines
- **Analyze Data**: Gain insights through advanced analytics and machine learning
- **Scale Operations**: Handle enterprise-level workloads with confidence

## Key Features

### 🤖 AI Agent Management
- Pre-built agent templates for common use cases
- Custom agent development tools
- Real-time monitoring and performance tracking
- Scalable deployment options

### 🔄 Workflow Automation
- Visual workflow designer
- Integration with popular business tools
- Event-driven automation triggers
- Comprehensive audit trails

### 📊 Analytics & Insights
- Real-time dashboards
- Custom reporting tools
- Predictive analytics capabilities
- Data visualization components

### 🔒 Enterprise Security
- Role-based access control
- Data encryption at rest and in transit
- Compliance with industry standards
- Comprehensive audit logging

## Getting Started

1. **Sign Up**: Create your Nexus account
2. **Explore**: Browse the dashboard and available features
3. **Create**: Build your first AI agent or workflow
4. **Deploy**: Launch your solution in production
5. **Monitor**: Track performance and optimize

## Architecture

The Nexus platform is built on modern cloud-native architecture:

\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   Mobile App    │    │   API Client    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API Gateway   │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Agent Engine   │    │ Workflow Engine │    │ Analytics Engine│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Data Layer    │
                    └─────────────────┘
\`\`\`

## Next Steps

Ready to dive deeper? Check out these resources:

- [Quick Start Guide](/docs/quick-start) - Get up and running in 5 minutes
- [Basic Concepts](/docs/basic-concepts) - Learn the fundamental concepts
- [First AI Project](/docs/first-ai-project) - Create your first AI project

Need help? Our [support team](/support) is here to assist you.
    `
  },
  {
    id: 'quick-start',
    title: 'Quick Start Guide',
    description: 'Get up and running with the Nexus platform in 5 minutes',
    slug: 'quick-start',
    sectionId: 'getting-started',
    order: 2,
    difficulty: 'beginner',
    tags: ['quickstart', 'setup', 'tutorial'],
    lastUpdated: '2024-07-04',
    readTime: 8,
    prerequisites: ['platform-overview'],
    content: `
# Quick Start Guide

This guide will help you get started with the Nexus platform in just 5 minutes.

## Prerequisites

- A valid email address
- Basic understanding of AI concepts (helpful but not required)

## Step 1: Create Your Account

1. Visit the [Nexus platform](https://nexus.aic.com)
2. Click "Sign Up" in the top right corner
3. Fill in your details:
   - Email address
   - Company name
   - Password
4. Verify your email address

## Step 2: Complete Your Profile

After email verification:

1. **Company Information**
   - Industry sector
   - Company size
   - Use case interests

2. **Role Setup**
   - Your role in the organization
   - Technical experience level
   - Areas of interest

## Step 3: Explore the Dashboard

Your dashboard provides an overview of:

- **Active Projects**: Current AI projects and workflows
- **System Health**: Platform status and performance metrics
- **Recent Activity**: Latest actions and updates
- **Quick Actions**: Common tasks and shortcuts

### Dashboard Components

\`\`\`typescript
interface DashboardData {
  projects: {
    active: number
    completed: number
    inProgress: number
  }
  agents: {
    deployed: number
    training: number
    idle: number
  }
  workflows: {
    running: number
    scheduled: number
    failed: number
  }
}
\`\`\`

## Step 4: Create Your First AI Agent

Let's create a simple customer service agent:

1. **Navigate to Agents**
   - Click "AI Agents" in the sidebar
   - Click "Create New Agent"

2. **Choose Template**
   - Select "Customer Service Agent"
   - Review the template description

3. **Configure Agent**
   \`\`\`json
   {
     "name": "Customer Support Bot",
     "description": "Handles basic customer inquiries",
     "language": "English",
     "personality": "Professional and helpful",
     "knowledgeBase": "FAQ documents"
   }
   \`\`\`

4. **Train Agent**
   - Upload your FAQ documents
   - Add sample conversations
   - Test responses

5. **Deploy Agent**
   - Choose deployment environment
   - Configure integration settings
   - Launch the agent

## Step 5: Monitor Performance

Once deployed, monitor your agent:

- **Response Accuracy**: How well the agent answers questions
- **Response Time**: Average time to respond
- **User Satisfaction**: Feedback scores
- **Conversation Volume**: Number of interactions

### Monitoring Dashboard

\`\`\`javascript
// Example monitoring data
const agentMetrics = {
  accuracy: 94.5,
  avgResponseTime: 1.2, // seconds
  satisfaction: 4.6, // out of 5
  dailyConversations: 247
}
\`\`\`

## Common First Steps

### For Developers
- Explore the [API Reference](/docs/api-reference)
- Set up [authentication](/docs/authentication)
- Try the [SDKs](/docs/sdks)

### For Business Users
- Create [workflows](/docs/workflows)
- Set up [integrations](/docs/integrations)
- Configure [analytics](/docs/analytics)

### For Administrators
- Manage [user permissions](/docs/user-management)
- Configure [security settings](/docs/security)
- Set up [audit logging](/docs/audit-logs)

## Troubleshooting

### Common Issues

**Agent not responding?**
- Check training data quality
- Verify deployment status
- Review error logs

**Slow performance?**
- Monitor resource usage
- Check network connectivity
- Review system status

**Integration problems?**
- Verify API credentials
- Check endpoint configurations
- Review webhook settings

## Next Steps

Now that you're set up, explore these advanced features:

1. **[Workflow Automation](/docs/workflows)** - Automate business processes
2. **[Data Integration](/docs/data-integration)** - Connect your data sources
3. **[Advanced Analytics](/docs/analytics)** - Gain deeper insights
4. **[Custom Development](/docs/custom-development)** - Build custom solutions

## Getting Help

Need assistance? We're here to help:

- 📚 Browse our [comprehensive documentation](/docs)
- 💬 Join our [community forum](https://community.aic.com)
- 📧 Contact [support@aic.com](mailto:support@aic.com)
- 📞 Call our support line: 1-800-AIC-HELP

Welcome to the future of AI-powered business automation!
    `
  }
]
