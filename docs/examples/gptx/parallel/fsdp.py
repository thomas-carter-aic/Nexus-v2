"""
Fully Sharded Data Parallel (FSDP) setup for model sharding.
Useful for larger models beyond Free-Tier.
"""

import torch
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.wrap import default_auto_wrap_policy

def fsdp_wrap_model(model, auto_wrap=True):
    if auto_wrap:
        return FSDP(model, auto_wrap_policy=default_auto_wrap_policy)
    else:
        return FSDP(model)
