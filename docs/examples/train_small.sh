#!/bin/bash
# Minimal training demo for Free-Tier
python gptx/train/trainer.py \
    --epochs 1 \
    --batch_size 1 \
    --max_seq_len 32 \
    --dataset data/sample_train.jsonl
