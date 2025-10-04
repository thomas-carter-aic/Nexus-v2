# Bounded Contexts

*Date:* 2025-09-18 
*Status:* Draft 
*Deciders:* Architecture Team

## Goal
Partition the domain into logical contexts to reduce coupling. Each bounded context will become an isolated microservice or service package.

## Identified Bounded Contexts

1. **User Management & Access Control (UserMgmt)**
   - Manages users, roles, tenants, permissions
   - Sync APIs: REST/gRPC/GraphQL
   - Async Events: SecurityAlerts, RoleChanged

2. **Model Lifecycle Management (MLM)**
   - Manages models, experiments, deployments
   - Events: ModelDeployed, ModelVersionUpdated
   - Subscribers: AI Inference, Billing, Data Pipelines

3. **Data & Feature Pipelines**
   - Manages datasets, transformations, feature sets
   - Events: FeatureUpdated, DatasetIngested
   - Subscribers: MLM, AI Inference

4. **AI Inference & Serving**
   - Manages inference jobs, endpoints, service instances
   - Events: InferenceCompleted
   - Subscribers: Billing, Observability

5. **Billing & Usage**
   - Manages accounts, subscriptions, invoices, usage records
   - Events: InvoiceGenerated
   - Subscribers: External Integrations, Observability

6. **Observability & Monitoring**
   - Tracks metrics, logs, traces, and alerts
   - Subscribers: All other contexts

7. **External Integrations**
   - Manages API connectors, webhooks, and plugins
   - Subscribers: MLM, Billing, Observability

### Notes
- Each bounded context is a **microservice**.
- Each context maintains its own **database and repositories**.
- Contexts communicate via **async events** and **sync APIs**.
