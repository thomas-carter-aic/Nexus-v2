"""
Simplified DPO trainer for Free-Tier mini-GPT.
Handles reward-model-guided policy updates (demo only).
"""

import torch
from gptx.train.trainer import Trainer

class DPOMiniTrainer(Trainer):
    def reward_step(self, logits, rewards):
        """
        Apply reward-guided gradient adjustment (simplified)
        """
        loss = -torch.mean(logits * rewards)  # placeholder
        loss.backward()
        self.optimizer.step()
        return loss.item()
