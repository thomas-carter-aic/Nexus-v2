"""
Mini GPT-2 implementation (Free-Tier CPU demo)
"""

from torch import nn
import torch
from gptx.modules.block import GPTBlock

class GPT2Small(nn.Module):
    def __init__(self, vocab_size=50257, d_model=128, n_layers=2, n_heads=4, max_seq_len=32):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList([GPTBlock(d_model=d_model, n_heads=n_heads) for _ in range(n_layers)])
        self.ln = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, x):
        B, T = x.shape
        x = self.token_emb(x) + self.pos_emb(torch.arange(T, device=x.device))
        for block in self.blocks:
            x = block(x)
        x = self.ln(x)
        return self.head(x)
