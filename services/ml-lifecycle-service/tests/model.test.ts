import { ModelFactory } from '../src/factories/model-factory'

describe('Model Aggregate', () => {
  it('should create a new model in draft status', () => {
    const model = ModelFactory.create('MyModel')
    expect(model.status).toBe('draft')
    expect(model.version).toBe(1)
  })
})
