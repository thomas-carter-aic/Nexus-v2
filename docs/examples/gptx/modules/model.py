"""
Full GPT model: stacks N GPTBlocks + embedding + output projection.
Supports variable depth, width, and context length.
"""

import torch.nn as nn
from .block import GPTBlock

class GPTModel(nn.Module):
    def __init__(self, vocab_size: int, d_model: int = 512, n_layers: int = 6, n_heads: int = 8, max_seq_len: int = 512):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = nn.Parameter(nn.init.normal_(nn.Parameter(torch.empty(max_seq_len, d_model)), std=0.01))
        self.blocks = nn.ModuleList([GPTBlock(d_model, n_heads) for _ in range(n_layers)])
        self.ln_f = nn.LayerNorm(d_model)
        self.output_proj = nn.Linear(d_model, vocab_size, bias=False)
    
    def forward(self, input_ids):
        x = self.token_embedding(input_ids) + self.pos_embedding[:input_ids.size(1), :]
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        logits = self.output_proj(x)
        return logits
