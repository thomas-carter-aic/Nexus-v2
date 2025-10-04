/**
 * Factory: UserFactory
 * Responsible for creating new User aggregates
 */
export class UserFactory {
  static create(email: string, role: string) {
    return { id: 'generated-id', email, role, status: 'active' };
  }
}
