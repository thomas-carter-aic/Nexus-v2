#!/bin/bash
# Profile training run on Free-Tier CPU

echo "Starting mini-GPT training profile..."
python -m cProfile -o profile.out training/train.py
echo "Profile saved to profile.out"
