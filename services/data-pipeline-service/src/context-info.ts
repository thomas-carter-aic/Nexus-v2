/**
 * Bounded Context: Data & Feature Pipelines
 * Aggregates: FeatureStore, Dataset, Transformation, FeatureSet
 * Events Published: FeatureUpdated, DatasetIngested
 * Subscribers: ML Lifecycle, AI Inference
 * Database: PostgreSQL / Data Lake per context
 * Notes:
 * - Handles ingestion, transformation, and feature engineering.
 * - Publishes async events for model training and inference.
 */
export const CONTEXT_INFO = {
  name: 'Data & Feature Pipelines',
  aggregates: ['FeatureStore', 'Dataset', 'Transformation', 'FeatureSet'],
  eventsPublished: ['FeatureUpdated', 'DatasetIngested'],
  subscribers: ['MLLifecycleService', 'AIInferenceService'],
};
