"""
Compute pseudo-perplexity on small test dataset
"""

import torch
from gptx.train.loss import CausalLMLoss

def eval_perplexity(model, dataset):
    criterion = CausalLMLoss()
    total_loss = 0
    total_tokens = 0
    model.eval()
    with torch.no_grad():
        for batch in dataset:
            input_ids = batch["input_ids"]
            logits = model(input_ids)
            loss = criterion(logits, input_ids)
            total_loss += loss.item() * input_ids.numel()
            total_tokens += input_ids.numel()
    perplexity = torch.exp(torch.tensor(total_loss / total_tokens))
    return perplexity.item()
