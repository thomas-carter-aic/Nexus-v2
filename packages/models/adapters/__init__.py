"""
Adapter modules for parameter-efficient fine-tuning (LoRA / adapters)
"""

from torch import nn

class Adapter(nn.Module):
    def __init__(self, input_dim, bottleneck=32):
        super().__init__()
        self.down = nn.Linear(input_dim, bottleneck)
        self.up = nn.Linear(bottleneck, input_dim)

    def forward(self, x):
        return self.up(self.down(x)) + x
