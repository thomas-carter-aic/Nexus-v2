#!/bin/bash
# Pretrain mini-GPT with long context sequences (demo)
python gptx/train/trainer.py \
    --epochs 1 \
    --batch_size 1 \
    --max_seq_len 128 \
    --dataset data/sample_train.jsonl
