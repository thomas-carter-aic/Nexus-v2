#!/bin/bash
# Serve mini-GPT with vLLM runner
python gptx/serve/vllm_runner.py \
    --model_path checkpoints/step_10.pt
