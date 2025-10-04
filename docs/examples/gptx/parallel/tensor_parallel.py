"""
Tensor Parallelism: splits linear layers across GPUs.
Useful for very wide models (d_model >> 1024)
"""

import torch
import torch.distributed as dist

class ColumnParallelLinear(torch.nn.Module):
    """Splits output dimension across GPUs"""
    def __init__(self, in_features, out_features):
        super().__init__()
        self.world_size = dist.get_world_size()
        self.rank = dist.get_rank()
        self.local_out = out_features // self.world_size
        self.linear = torch.nn.Linear(in_features, self.local_out)

    def forward(self, x):
        out = self.linear(x)
        # optionally all-gather across GPUs here for full output
        return out
