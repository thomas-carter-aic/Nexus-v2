export interface ModelDeployedEvent {
  modelId: string;
  version: number;
  deployedAt: string;
}

export interface ModelVersionUpdatedEvent {
  modelId: string;
  oldVersion: number;
  newVersion: number;
  updatedAt: string;
}
