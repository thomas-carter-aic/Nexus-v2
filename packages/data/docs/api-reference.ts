import { DocArticle } from '@/types/docs'

export const apiReferenceArticles: DocArticle[] = [
  {
    id: 'rest-api-reference',
    title: 'REST API Reference',
    description: 'Complete REST API documentation with examples and response schemas',
    slug: 'rest-api-reference',
    sectionId: 'api-reference',
    order: 1,
    difficulty: 'intermediate',
    tags: ['api', 'rest', 'reference', 'endpoints'],
    lastUpdated: '2024-07-04',
    readTime: 15,
    content: `
# REST API Reference

The Nexus REST API provides programmatic access to all platform features. This reference covers all available endpoints, request/response formats, and authentication methods.

## Base URL

All API requests should be made to:

\`\`\`
https://api.nexus.aic.com/v1
\`\`\`

## Authentication

All API requests require authentication using API keys or OAuth 2.0 tokens.

### API Key Authentication

Include your API key in the request header:

\`\`\`http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
\`\`\`

### OAuth 2.0 Authentication

For user-specific operations, use OAuth 2.0:

\`\`\`http
Authorization: Bearer YOUR_OAUTH_TOKEN
Content-Type: application/json
\`\`\`

## Rate Limiting

API requests are rate-limited to ensure fair usage:

- **Free Tier**: 1,000 requests per hour
- **Pro Tier**: 10,000 requests per hour
- **Enterprise**: Custom limits

Rate limit headers are included in all responses:

\`\`\`http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1625097600
\`\`\`

## Agents API

### List Agents

Get all AI agents in your organization.

\`\`\`http
GET /agents
\`\`\`

**Parameters:**
- \`page\` (integer): Page number (default: 1)
- \`limit\` (integer): Items per page (default: 20, max: 100)
- \`status\` (string): Filter by status (\`active\`, \`inactive\`, \`training\`)

**Response:**

\`\`\`json
{
  "data": [
    {
      "id": "agent_123",
      "name": "Customer Support Bot",
      "description": "Handles customer inquiries",
      "status": "active",
      "created_at": "2024-07-01T10:00:00Z",
      "updated_at": "2024-07-04T15:30:00Z",
      "metrics": {
        "accuracy": 94.5,
        "response_time": 1.2,
        "conversations": 1247
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5,
    "pages": 1
  }
}
\`\`\`

### Create Agent

Create a new AI agent.

\`\`\`http
POST /agents
\`\`\`

**Request Body:**

\`\`\`json
{
  "name": "Sales Assistant",
  "description": "Helps with sales inquiries and lead qualification",
  "template": "sales_agent",
  "configuration": {
    "language": "en",
    "personality": "professional",
    "knowledge_base": ["sales_docs", "product_catalog"]
  }
}
\`\`\`

**Response:**

\`\`\`json
{
  "id": "agent_124",
  "name": "Sales Assistant",
  "description": "Helps with sales inquiries and lead qualification",
  "status": "training",
  "created_at": "2024-07-04T16:00:00Z",
  "training_progress": 0
}
\`\`\`

### Get Agent Details

Retrieve detailed information about a specific agent.

\`\`\`http
GET /agents/{agent_id}
\`\`\`

**Response:**

\`\`\`json
{
  "id": "agent_123",
  "name": "Customer Support Bot",
  "description": "Handles customer inquiries",
  "status": "active",
  "configuration": {
    "language": "en",
    "personality": "helpful",
    "knowledge_base": ["faq_docs", "support_articles"]
  },
  "metrics": {
    "accuracy": 94.5,
    "response_time": 1.2,
    "conversations_today": 47,
    "conversations_total": 1247,
    "satisfaction_score": 4.6
  },
  "created_at": "2024-07-01T10:00:00Z",
  "updated_at": "2024-07-04T15:30:00Z"
}
\`\`\`

### Update Agent

Update an existing agent's configuration.

\`\`\`http
PUT /agents/{agent_id}
\`\`\`

**Request Body:**

\`\`\`json
{
  "name": "Updated Customer Support Bot",
  "description": "Enhanced customer support with multilingual capabilities",
  "configuration": {
    "language": ["en", "es", "fr"],
    "personality": "friendly",
    "knowledge_base": ["faq_docs", "support_articles", "multilingual_docs"]
  }
}
\`\`\`

### Delete Agent

Delete an agent (this action is irreversible).

\`\`\`http
DELETE /agents/{agent_id}
\`\`\`

**Response:**

\`\`\`json
{
  "message": "Agent deleted successfully",
  "deleted_at": "2024-07-04T16:30:00Z"
}
\`\`\`

## Workflows API

### List Workflows

Get all workflows in your organization.

\`\`\`http
GET /workflows
\`\`\`

**Parameters:**
- \`status\` (string): Filter by status (\`active\`, \`paused\`, \`draft\`)
- \`category\` (string): Filter by category

**Response:**

\`\`\`json
{
  "data": [
    {
      "id": "workflow_456",
      "name": "Lead Processing",
      "description": "Automated lead qualification and routing",
      "status": "active",
      "trigger": "webhook",
      "steps": 5,
      "executions": 234,
      "success_rate": 98.7,
      "created_at": "2024-06-15T09:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 3,
    "pages": 1
  }
}
\`\`\`

### Create Workflow

Create a new automation workflow.

\`\`\`http
POST /workflows
\`\`\`

**Request Body:**

\`\`\`json
{
  "name": "Email Campaign Automation",
  "description": "Automated email sequences based on user behavior",
  "trigger": {
    "type": "event",
    "event": "user_signup"
  },
  "steps": [
    {
      "type": "delay",
      "duration": "1h"
    },
    {
      "type": "email",
      "template": "welcome_email",
      "recipient": "{{user.email}}"
    },
    {
      "type": "condition",
      "condition": "{{user.opened_email}}",
      "true_path": "send_followup",
      "false_path": "wait_24h"
    }
  ]
}
\`\`\`

## Analytics API

### Get Agent Analytics

Retrieve analytics data for a specific agent.

\`\`\`http
GET /agents/{agent_id}/analytics
\`\`\`

**Parameters:**
- \`period\` (string): Time period (\`1d\`, \`7d\`, \`30d\`, \`90d\`)
- \`metrics\` (array): Specific metrics to retrieve

**Response:**

\`\`\`json
{
  "agent_id": "agent_123",
  "period": "7d",
  "metrics": {
    "conversations": {
      "total": 342,
      "daily_average": 48.9,
      "trend": "+12.5%"
    },
    "accuracy": {
      "current": 94.5,
      "previous": 92.1,
      "trend": "+2.4%"
    },
    "response_time": {
      "average": 1.2,
      "p95": 2.8,
      "trend": "-0.3s"
    },
    "satisfaction": {
      "score": 4.6,
      "responses": 89,
      "trend": "+0.2"
    }
  },
  "time_series": [
    {
      "date": "2024-07-01",
      "conversations": 45,
      "accuracy": 93.2,
      "response_time": 1.4
    }
  ]
}
\`\`\`

## Error Handling

The API uses standard HTTP status codes and returns detailed error information:

### Error Response Format

\`\`\`json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ],
    "request_id": "req_abc123"
  }
}
\`\`\`

### Common Error Codes

- \`400\` - Bad Request: Invalid request parameters
- \`401\` - Unauthorized: Invalid or missing authentication
- \`403\` - Forbidden: Insufficient permissions
- \`404\` - Not Found: Resource not found
- \`429\` - Too Many Requests: Rate limit exceeded
- \`500\` - Internal Server Error: Server error

## SDKs and Libraries

Official SDKs are available for popular programming languages:

- **JavaScript/Node.js**: \`npm install @aic/nexus-sdk\`
- **Python**: \`pip install nexus-sdk\`
- **Java**: Maven/Gradle dependency available
- **C#**: NuGet package available

### JavaScript SDK Example

\`\`\`javascript
import { NexusClient } from '@aic/nexus-sdk'

const client = new NexusClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.nexus.aic.com/v1'
})

// List agents
const agents = await client.agents.list()

// Create new agent
const newAgent = await client.agents.create({
  name: 'My Agent',
  template: 'customer_service'
})

// Get analytics
const analytics = await client.agents.getAnalytics('agent_123', {
  period: '7d'
})
\`\`\`

## Webhooks

Configure webhooks to receive real-time notifications about events in your Nexus account.

### Webhook Events

- \`agent.created\` - New agent created
- \`agent.updated\` - Agent configuration updated
- \`agent.deployed\` - Agent deployed to production
- \`workflow.executed\` - Workflow execution completed
- \`conversation.started\` - New conversation initiated
- \`conversation.ended\` - Conversation completed

### Webhook Payload Example

\`\`\`json
{
  "event": "agent.deployed",
  "timestamp": "2024-07-04T16:45:00Z",
  "data": {
    "agent_id": "agent_123",
    "name": "Customer Support Bot",
    "deployment_id": "deploy_789",
    "environment": "production"
  }
}
\`\`\`

For more information about webhooks, see the [Webhooks Guide](/docs/webhooks).
    `
  },
  {
    id: 'authentication',
    title: 'Authentication',
    description: 'API authentication methods, security best practices, and token management',
    slug: 'authentication',
    sectionId: 'api-reference',
    order: 2,
    difficulty: 'intermediate',
    tags: ['authentication', 'security', 'api-keys', 'oauth'],
    lastUpdated: '2024-07-04',
    readTime: 10,
    content: `
# Authentication

The Nexus API supports multiple authentication methods to ensure secure access to your data and resources.

## Authentication Methods

### 1. API Key Authentication

API keys are the simplest way to authenticate API requests. They're ideal for server-to-server communication.

#### Getting Your API Key

1. Log in to your Nexus dashboard
2. Navigate to **Settings** → **API Keys**
3. Click **Generate New Key**
4. Copy and securely store your key

#### Using API Keys

Include your API key in the \`Authorization\` header:

\`\`\`http
GET /agents HTTP/1.1
Host: api.nexus.aic.com
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
\`\`\`

#### API Key Best Practices

- **Keep keys secure**: Never expose API keys in client-side code
- **Use environment variables**: Store keys in environment variables
- **Rotate regularly**: Generate new keys periodically
- **Limit scope**: Use different keys for different environments

\`\`\`bash
# Environment variable example
export NEXUS_API_KEY="nxs_live_abc123..."
\`\`\`

### 2. OAuth 2.0 Authentication

OAuth 2.0 is recommended for applications that act on behalf of users. It provides secure, token-based authentication with fine-grained permissions.

#### OAuth Flow

1. **Authorization Request**: Redirect user to Nexus authorization server
2. **User Consent**: User grants permissions to your application
3. **Authorization Code**: Nexus redirects back with authorization code
4. **Token Exchange**: Exchange code for access token
5. **API Access**: Use access token for API requests

#### Step 1: Authorization Request

Redirect users to:

\`\`\`
https://auth.nexus.aic.com/oauth/authorize?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  scope=agents:read agents:write workflows:read&
  state=RANDOM_STATE_STRING
\`\`\`

#### Step 2: Token Exchange

Exchange the authorization code for an access token:

\`\`\`http
POST /oauth/token HTTP/1.1
Host: auth.nexus.aic.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=AUTHORIZATION_CODE&
client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
redirect_uri=YOUR_REDIRECT_URI
\`\`\`

**Response:**

\`\`\`json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200...",
  "scope": "agents:read agents:write workflows:read"
}
\`\`\`

#### Step 3: Using Access Tokens

\`\`\`http
GET /agents HTTP/1.1
Host: api.nexus.aic.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
\`\`\`

### 3. JWT Tokens

For enterprise customers, we support custom JWT tokens signed with your private key.

#### JWT Claims

\`\`\`json
{
  "iss": "your-organization",
  "sub": "user-id",
  "aud": "nexus-api",
  "exp": 1625097600,
  "iat": 1625094000,
  "scope": "agents:read workflows:write"
}
\`\`\`

## Scopes and Permissions

Control access to different parts of the API using scopes:

### Available Scopes

| Scope | Description |
|-------|-------------|
| \`agents:read\` | Read agent information and metrics |
| \`agents:write\` | Create, update, and delete agents |
| \`workflows:read\` | Read workflow information and execution history |
| \`workflows:write\` | Create, update, and delete workflows |
| \`analytics:read\` | Access analytics and reporting data |
| \`admin:read\` | Read organization and user information |
| \`admin:write\` | Manage organization settings and users |

### Scope Examples

\`\`\`javascript
// Read-only access to agents and workflows
const scopes = ['agents:read', 'workflows:read']

// Full access to agents, read access to analytics
const scopes = ['agents:read', 'agents:write', 'analytics:read']

// Admin access (use carefully)
const scopes = ['admin:read', 'admin:write']
\`\`\`

## Security Best Practices

### 1. Token Storage

**Client-side applications:**
- Store tokens in memory or secure storage
- Never store in localStorage or cookies without proper security
- Use secure, httpOnly cookies when possible

**Server-side applications:**
- Store in environment variables or secure key management systems
- Use encrypted storage for long-term persistence

### 2. Token Refresh

Implement automatic token refresh for long-running applications:

\`\`\`javascript
class NexusClient {
  async refreshToken() {
    const response = await fetch('https://auth.nexus.aic.com/oauth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: this.refreshToken,
        client_id: this.clientId,
        client_secret: this.clientSecret
      })
    })
    
    const tokens = await response.json()
    this.accessToken = tokens.access_token
    this.refreshToken = tokens.refresh_token
  }
  
  async makeRequest(url, options = {}) {
    try {
      return await this.request(url, options)
    } catch (error) {
      if (error.status === 401) {
        await this.refreshToken()
        return await this.request(url, options)
      }
      throw error
    }
  }
}
\`\`\`

### 3. Rate Limiting

Respect rate limits to avoid being blocked:

\`\`\`javascript
class RateLimiter {
  constructor(requestsPerSecond = 10) {
    this.requestsPerSecond = requestsPerSecond
    this.requests = []
  }
  
  async throttle() {
    const now = Date.now()
    this.requests = this.requests.filter(time => now - time < 1000)
    
    if (this.requests.length >= this.requestsPerSecond) {
      const waitTime = 1000 - (now - this.requests[0])
      await new Promise(resolve => setTimeout(resolve, waitTime))
    }
    
    this.requests.push(now)
  }
}
\`\`\`

### 4. Error Handling

Handle authentication errors gracefully:

\`\`\`javascript
async function handleApiRequest(request) {
  try {
    const response = await fetch(request)
    
    if (response.status === 401) {
      // Token expired or invalid
      await refreshToken()
      return await fetch(request)
    }
    
    if (response.status === 403) {
      // Insufficient permissions
      throw new Error('Insufficient permissions for this operation')
    }
    
    if (response.status === 429) {
      // Rate limit exceeded
      const retryAfter = response.headers.get('Retry-After')
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000))
      return await fetch(request)
    }
    
    return response
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}
\`\`\`

## Testing Authentication

Use our test endpoints to verify your authentication setup:

### Test API Key

\`\`\`http
GET /auth/test HTTP/1.1
Host: api.nexus.aic.com
Authorization: Bearer YOUR_API_KEY
\`\`\`

**Response:**

\`\`\`json
{
  "authenticated": true,
  "key_id": "key_abc123",
  "scopes": ["agents:read", "agents:write"],
  "rate_limit": {
    "limit": 1000,
    "remaining": 999,
    "reset": 1625097600
  }
}
\`\`\`

### Test OAuth Token

\`\`\`http
GET /auth/user HTTP/1.1
Host: api.nexus.aic.com
Authorization: Bearer YOUR_OAUTH_TOKEN
\`\`\`

**Response:**

\`\`\`json
{
  "user_id": "user_123",
  "email": "user@example.com",
  "organization": "Acme Corp",
  "scopes": ["agents:read", "workflows:read"],
  "token_expires": "2024-07-04T17:00:00Z"
}
\`\`\`

## Troubleshooting

### Common Issues

**401 Unauthorized**
- Check that your API key or token is correct
- Verify the token hasn't expired
- Ensure you're using the correct authentication method

**403 Forbidden**
- Check that your token has the required scopes
- Verify your organization has access to the requested resource
- Contact support if you believe this is an error

**429 Too Many Requests**
- Implement rate limiting in your application
- Use exponential backoff for retries
- Consider upgrading your plan for higher limits

For additional help, contact our support team at [support@aic.com](mailto:support@aic.com).
    `
  }
]
