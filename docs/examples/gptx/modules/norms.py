"""
Normalization modules for GPT.
Supports LayerNorm with optional RMSNorm hook.
"""

import torch.nn as nn

class LayerNorm(nn.Module):
    def __init__(self, d_model: int, eps: float = 1e-5):
        super().__init__()
        self.norm = nn.LayerNorm(d_model, eps=eps)
    
    def forward(self, x):
        return self.norm(x)

class RMSNorm(nn.Module):
    """Optional RMSNorm (used in some GPT variants)"""
    def __init__(self, d_model: int, eps: float = 1e-8):
        super().__init__()
        self.eps = eps
        self.scale = nn.Parameter(torch.ones(d_model))
    
    def forward(self, x):
        norm = x.norm(dim=-1, keepdim=True)
        return self.scale * x / (norm + self.eps)
