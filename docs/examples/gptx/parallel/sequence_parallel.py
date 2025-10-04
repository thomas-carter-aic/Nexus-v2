"""
Sequence Parallelism: splits sequence dimension across GPUs.
Useful for extremely long context models (32k+ tokens)
"""

import torch
import torch.distributed as dist

def split_sequences(x):
    """
    Splits sequence dimension for sequence parallelism
    x: (batch, seq_len, hidden)
    Returns: local shard
    """
    world_size = dist.get_world_size()
    seq_len = x.size(1)
    shard_size = seq_len // world_size
    rank = dist.get_rank()
    return x[:, rank*shard_size:(rank+1)*shard_size, :]
