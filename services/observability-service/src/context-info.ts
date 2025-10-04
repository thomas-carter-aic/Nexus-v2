/**
 * Bounded Context: Observability & Monitoring
 * Aggregates: Metrics, Logs, Traces, Alerts, AlertRules
 * Events Published: MetricCaptured, AlertTriggered
 * Subscribers: None (central observability context)
 * Database: Time-series DB (Prometheus / InfluxDB)
 * Notes:
 * - Central monitoring context collecting events from all other services.
 * - Provides dashboards, alerting, and tracing.
 */
export const CONTEXT_INFO = {
  name: 'Observability & Monitoring',
  aggregates: ['Metrics', 'Logs', 'Traces', 'Alerts', 'AlertRules'],
  eventsPublished: ['MetricCaptured', 'AlertTriggered'],
  subscribers: [],
};
