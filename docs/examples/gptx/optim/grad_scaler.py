"""
Gradient scaler for mixed precision training.
Useful for Free-Tier FP16 experiments or full-scale AMP training.
"""

import torch

class SimpleGradScaler:
    """Lightweight grad scaler, mimics torch.cuda.amp.GradScaler"""
    def __init__(self, init_scale=2.0**16, growth_factor=2.0, backoff_factor=0.5, growth_interval=2000):
        self.scale = init_scale
        self.growth_factor = growth_factor
        self.backoff_factor = backoff_factor
        self.growth_interval = growth_interval
        self._growth_tracker = 0

    def scale_loss(self, loss):
        return loss * self.scale

    def unscale_(self, optimizer):
        for group in optimizer.param_groups:
            for p in group['params']:
                if p.grad is not None:
                    p.grad.data.div_(self.scale)

    def update(self, found_inf=False):
        if found_inf:
            self.scale *= self.backoff_factor
            self._growth_tracker = 0
        else:
            self._growth_tracker += 1
            if self._growth_tracker % self.growth_interval == 0:
                self.scale *= self.growth_factor
