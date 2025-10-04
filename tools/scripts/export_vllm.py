"""
Export model for vLLM serving (Free-Tier CPU demo)
"""

import torch
from gptx.modules.model import GPTModel

if __name__ == "__main__":
    model = GPTModel(vocab_size=50257, d_model=128, n_layers=2, n_heads=4, max_seq_len=32)
    torch.save(model.state_dict(), "models/mini_gpt_vllm.pt")
    print("Saved mini-GPT vLLM model to models/mini_gpt_vllm.pt")
