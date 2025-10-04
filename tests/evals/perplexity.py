"""
Compute pseudo-perplexity on small dataset for Free-Tier mini-GPT.
"""

import torch
from torch.utils.data import DataLoader
from gptx.modules.model import GPTModel
from gptx.train.loss import CausalLMLoss

vocab_size = 50257
model = GPTModel(vocab_size=vocab_size, d_model=128, n_layers=2, n_heads=4, max_seq_len=128)
model.eval()

dataset = [{"input_ids": torch.randint(0, vocab_size, (32,))} for _ in range(10)]
dataloader = DataLoader(dataset, batch_size=2)

criterion = CausalLMLoss()

total_loss = 0.0
total_tokens = 0

with torch.no_grad():
    for batch in dataloader:
        input_ids = torch.stack([b["input_ids"] for b in batch])
        logits = model(input_ids)
        loss = criterion(logits, input_ids)
        total_loss += loss.item() * input_ids.numel()
        total_tokens += input_ids.numel()

perplexity = torch.exp(torch.tensor(total_loss / total_tokens))
print(f"Perplexity: {perplexity:.2f}")
