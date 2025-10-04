"""
Single GPT Transformer block: Attention + MLP + Residual + Norm
"""

import torch.nn as nn
from .attention import CausalSelfAttention
from .mlp import MLP
from .norms import LayerNorm

class GPTBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()
        self.attn = CausalSelfAttention(d_model, n_heads, dropout)
        self.ln1 = LayerNorm(d_model)
        self.mlp = MLP(d_model)
        self.ln2 = LayerNorm(d_model)
    
    def forward(self, x, mask=None):
        # Attention + residual
        x = x + self.attn(self.ln1(x), mask)
        # MLP + residual
        x = x + self.mlp(self.ln2(x))
        return x
