"""
Standalone PyTorch inference server.
Handles batch generation on CPU/GPU for Free-Tier mini-GPT.
"""

import torch
from gptx.modules.model import GPTModel

vocab_size = 50257
model = GPTModel(vocab_size=vocab_size, d_model=128, n_layers=2, n_heads=4, max_seq_len=128)
model.eval()

def generate(prompt: str, max_new_tokens: int = 32):
    input_ids = torch.tensor([[ord(c) % vocab_size for c in prompt]])
    generated = input_ids.tolist()[0]
    for _ in range(max_new_tokens):
        with torch.no_grad():
            logits = model(input_ids)
            next_token = torch.argmax(logits[:, -1, :], dim=-1)
            generated.append(next_token.item())
            input_ids = torch.tensor([generated])
    return "".join([chr(t) for t in generated])
