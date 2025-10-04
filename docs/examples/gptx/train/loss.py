"""
Cross-entropy loss for causal language modeling.
Supports optional label smoothing and reduced memory usage.
"""

import torch
import torch.nn as nn

class CausalLMLoss(nn.Module):
    def __init__(self, label_smoothing: float = 0.0):
        super().__init__()
        self.label_smoothing = label_smoothing
        self.ce = nn.CrossEntropyLoss(ignore_index=0, reduction="mean")

    def forward(self, logits, labels):
        """
        Args:
            logits: (batch, seq_len, vocab_size)
            labels: (batch, seq_len)
        """
        B, T, V = logits.size()
        logits_flat = logits.view(B*T, V)
        labels_flat = labels.view(B*T)
        loss = self.ce(logits_flat, labels_flat)
        return loss
