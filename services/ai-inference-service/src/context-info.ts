/**
 * Bounded Context: AI Inference & Serving
 * Aggregates: InferenceJob, Endpoint, ServiceInstance
 * Events Published: InferenceCompleted
 * Subscribers: Billing, Observability
 * Database: PostgreSQL / Redis per context
 * Notes:
 * - Handles inference requests and job lifecycle.
 * - Publishes async events on completion for billing and monitoring.
 */
export const CONTEXT_INFO = {
  name: 'AI Inference & Serving',
  aggregates: ['InferenceJob', 'Endpoint', 'ServiceInstance'],
  eventsPublished: ['InferenceCompleted'],
  subscribers: ['BillingService', 'ObservabilityService'],
};
