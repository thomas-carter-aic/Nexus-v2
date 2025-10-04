import { UserFactory } from '../src/factories/user-factory'

describe('User Aggregate', () => {
  it('should create a new user with active status', () => {
    const user = UserFactory.create('test@example.com', 'admin')
    expect(user.status).toBe('active')
    expect(user.role).toBe('admin')
  })
})
