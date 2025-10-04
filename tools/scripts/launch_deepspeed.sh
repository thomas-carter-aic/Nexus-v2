#!/bin/bash
# Launch DeepSpeed training placeholder

echo "Launching DeepSpeed training (Free-Tier CPU demo)"
deepspeed training/train.py --deepspeed configs/train/deepspeed_zero3.json
