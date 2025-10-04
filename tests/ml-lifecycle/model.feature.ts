Feature: Model Deployment
  Scenario: Deploy a trained model
    Given a trained model version 1
    When the model is deployed
    Then it becomes active
