"""
Initialize Deepspeed for distributed training.
Free-Tier demo supports single GPU, hooks for multi-node scaling.
"""

import deepspeed

def init_deepspeed(model, optimizer=None, config_file=None):
    """
    Returns (model_engine, optimizer, _, _)
    """
    model_engine, optimizer, _, _ = deepspeed.initialize(
        model=model,
        optimizer=optimizer,
        config=config_file
    )
    return model_engine, optimizer
