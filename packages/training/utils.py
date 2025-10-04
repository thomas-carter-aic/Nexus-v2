"""
Utility functions for training loops
"""

import torch

def move_to_device(batch, device):
    """
    Move a batch of tensors to the target device
    """
    return {k: v.to(device) for k, v in batch.items()}

def set_seed(seed=42):
    import random, numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
