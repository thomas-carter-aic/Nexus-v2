/**
 * Bounded Context: Model Lifecycle Management (MLM)
 * Aggregates: Model, Experiment, Deployment
 * Subdomain: Core Domain
 * Events Published: ModelDeployed, ModelVersionUpdated
 * Subscribers: AI Inference, Billing, Data Pipelines
 * Database: PostgreSQL (per context)
 * Notes:
 * - Maintains all domain logic for model lifecycle
 * - Communicates asynchronously with other contexts
 */
export const CONTEXT_INFO = {
  name: 'Model Lifecycle Management',
  aggregates: ['Model', 'Experiment', 'Deployment'],
  eventsPublished: ['ModelDeployed', 'ModelVersionUpdated'],
  subscribers: ['AIInferenceService', 'BillingService', 'DataPipelineService'],
};
