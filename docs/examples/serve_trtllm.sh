#!/bin/bash
# Serve mini-GPT with TRT fallback
python gptx/serve/trtllm_runner.py \
    --model_path checkpoints/step_10.pt
