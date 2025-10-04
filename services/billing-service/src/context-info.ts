/**
 * Bounded Context: Billing & Usage
 * Aggregates: BillingAccount, Subscription, UsageRecord, Invoice
 * Events Published: InvoiceGenerated, SubscriptionUpdated
 * Subscribers: External Integrations, Observability
 * Database: PostgreSQL / MySQL per context
 * Notes:
 * - Tracks usage, subscriptions, invoices, and payments.
 * - Publishes async events for external integrations and monitoring.
 */
export const CONTEXT_INFO = {
  name: 'Billing & Usage',
  aggregates: ['BillingAccount', 'Subscription', 'UsageRecord', 'Invoice'],
  eventsPublished: ['InvoiceGenerated', 'SubscriptionUpdated'],
  subscribers: ['ExternalIntegrationService', 'ObservabilityService'],
};
