# Red-Team Testing Plan

## Objectives
- Detect toxic or unsafe outputs
- Verify correct handling of unknown or adversarial prompts
- Ensure mini-GPT does not expose sensitive data

## Methodology
- Provide edge-case prompts
- Evaluate output filtering
- Record failures and update filters

## Notes
- Free-Tier PoC uses basic character-level checks
- Full-scale models require advanced content moderation and RLHF pipelines
