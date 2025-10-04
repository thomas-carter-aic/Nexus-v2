/**
 * Bounded Context: External Integrations
 * Aggregates: APIConnector, Webhook, Plugin, IntegrationAggregate
 * Events Published: IntegrationTriggered, ConnectorUpdated
 * Subscribers: ML Lifecycle, Billing, Observability
 * Database: PostgreSQL / MongoDB per context
 * Notes:
 * - Manages external API connectors, webhooks, and plugins.
 * - Subscribes to events from other contexts and triggers integrations.
 */
export const CONTEXT_INFO = {
  name: 'External Integrations',
  aggregates: ['APIConnector', 'Webhook', 'Plugin', 'IntegrationAggregate'],
  eventsPublished: ['IntegrationTriggered', 'ConnectorUpdated'],
  subscribers: ['MLLifecycleService', 'BillingService', 'ObservabilityService'],
};
