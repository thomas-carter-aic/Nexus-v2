"""
Training callbacks: checkpointing, logging, LR scheduling hooks.
"""

import os
import torch

class CheckpointCallback:
    """Save model every N steps"""
    def __init__(self, save_dir: str, save_steps: int = 100):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.save_steps = save_steps

    def maybe_save(self, model, step):
        if step % self.save_steps == 0:
            path = os.path.join(self.save_dir, f"step_{step}.pt")
            torch.save(model.state_dict(), path)
