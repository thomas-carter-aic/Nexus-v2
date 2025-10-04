/**
 * Bounded Context: User Management & Access Control (UserMgmt)
 * Aggregates: User, Role, Tenant, Permissions
 * Events Published: UserCreated, UserUpdated, RoleChanged
 * Subscribers: ExternalIntegrations, Observability
 * Database: PostgreSQL / MongoDB per context
 * Notes:
 * - Maintains all user, role, tenant, and permissions logic.
 * - Provides sync APIs for CRUD operations.
 * - Publishes async events for downstream systems.
 */
export const CONTEXT_INFO = {
  name: 'User Management & Access Control',
  aggregates: ['User', 'Role', 'Tenant', 'Permissions'],
  eventsPublished: ['UserCreated', 'UserUpdated', 'RoleChanged'],
  subscribers: ['ExternalIntegrationService', 'ObservabilityService'],
};
