"""
Benchmark inference latency for mini-GPT.
Measures average time per forward pass on CPU or GPU.
"""

import time
import torch
from gptx.modules.model import GPTModel

vocab_size = 50257
model = GPTModel(vocab_size=vocab_size, d_model=128, n_layers=2, n_heads=4, max_seq_len=128)
model.eval()

input_ids = torch.randint(0, vocab_size, (1, 32))  # demo input
n_trials = 50
times = []

with torch.no_grad():
    for _ in range(n_trials):
        start = time.time()
        _ = model(input_ids)
        times.append(time.time() - start)

avg_latency = sum(times) / len(times)
print(f"Average latency per forward pass: {avg_latency*1000:.2f} ms")
