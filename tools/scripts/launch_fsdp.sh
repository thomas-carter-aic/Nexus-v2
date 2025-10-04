#!/bin/bash
# Launch Fully Sharded Data Parallel (FSDP) training placeholder

echo "Launching FSDP training (Free-Tier CPU demo)"
python training/train.py --strategy fsdp
