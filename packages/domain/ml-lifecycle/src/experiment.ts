/**
 * Aggregate: Experiment
 * Subdomain: Model Lifecycle Management
 * Core Domain: YES
 *
 * Responsibilities:
 * - Maintain versioning and deployment state
 * - Track experiments
 *
 * References:
 * - ADR-001: Use DDD for bounded contexts
 * - docs/domain/core-domain.md
 */
export class Experiment {
  constructor(
    public id: string,
    public name: string,
    public version: number,
    public status: 'draft' | 'trained' | 'deployed'
  ) {}

  /**
   * Invariants:
   * - Version must increment sequentially
   * - Only one active deployment per environment
   */
  deploy() {
    /* stub for deploy logic */
  }
}
