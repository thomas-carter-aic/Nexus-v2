/**
 * Domain Events for User Management
 */

export interface UserCreatedEvent {
  userId: string;
  email: string;
  createdAt: string;
}

export interface UserUpdatedEvent {
  userId: string;
  updatedFields: string[];
  updatedAt: string;
}

export interface RoleChangedEvent {
  userId: string;
  oldRole: string;
  newRole: string;
  changedAt: string;
}
