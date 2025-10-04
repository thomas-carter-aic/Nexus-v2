"""
Learning rate schedulers.
Supports cosine decay, linear warmup, and multi-stage schedules.
"""

from torch.optim.lr_scheduler import LambdaLR
import math

def cosine_warmup_scheduler(optimizer, warmup_steps: int, total_steps: int, min_lr: float = 0.0):
    """
    Cosine decay with linear warmup.
    """
    def lr_lambda(step):
        if step < warmup_steps:
            return float(step) / float(max(1, warmup_steps))
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return max(min_lr, 0.5 * (1.0 + math.cos(math.pi * progress)))
    return LambdaLR(optimizer, lr_lambda)
