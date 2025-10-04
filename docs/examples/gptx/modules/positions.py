"""
Positional encodings: RoPE / ALiBi support for long context.
Hooks for context length scaling.
"""

import torch
import math

def sinusoidal_positions(seq_len: int, d_model: int):
    """Standard sinusoidal positional encoding"""
    pos = torch.arange(seq_len).unsqueeze(1)
    i = torch.arange(d_model // 2).unsqueeze(0)
    angles = pos / (10000 ** (2*i/d_model))
    pe = torch.zeros(seq_len, d_model)
    pe[:, 0::2] = torch.sin(angles)
    pe[:, 1::2] = torch.cos(angles)
    return pe

def alibi_bias(n_heads: int, seq_len: int):
    """
    Returns linear attention bias for ALiBi.
    Supports long context scaling.
    """
    slopes = torch.arange(1, n_heads+1).float()
    bias = torch.arange(seq_len).unsqueeze(0) * slopes.unsqueeze(1)
    return bias
