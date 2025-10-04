"""
Export model for TensorRT LLM serving (Free-Tier CPU demo)
"""

import torch
from gptx.modules.model import GPTModel

if __name__ == "__main__":
    model = GPTModel(vocab_size=50257, d_model=128, n_layers=2, n_heads=4, max_seq_len=32)
    torch.save(model.state_dict(), "models/mini_gpt_trtllm.pt")
    print("Saved mini-GPT TRT-LLM model to models/mini_gpt_trtllm.pt")
