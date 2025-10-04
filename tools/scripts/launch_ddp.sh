#!/bin/bash
# Launch Distributed Data Parallel (DDP) training placeholder

echo "Launching DDP training (Free-Tier CPU demo)"
python -m torch.distributed.run --nproc_per_node=1 training/train.py
