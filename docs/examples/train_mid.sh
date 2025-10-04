#!/bin/bash
# Mid-sized training demo
python gptx/train/trainer.py \
    --epochs 2 \
    --batch_size 2 \
    --max_seq_len 64 \
    --dataset data/sample_train.jsonl
