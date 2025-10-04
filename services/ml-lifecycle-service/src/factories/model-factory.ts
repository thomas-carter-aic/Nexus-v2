export class ModelFactory {
  static create(name: string) {
    return { id: 'generated-id', name, version: 1, status: 'draft' }
  }
}
