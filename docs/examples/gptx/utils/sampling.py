"""
Sampling utilities: greedy, top-k, top-p
"""

import torch

def greedy_sample(logits):
    return torch.argmax(logits, dim=-1)

def top_k_sample(logits, k=5):
    topk = torch.topk(logits, k, dim=-1)
    indices = topk.indices
    return indices[:, -1]

def top_p_sample(logits, p=0.9):
    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
    sorted_indices_to_remove = cumulative_probs > p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    logits[sorted_indices[sorted_indices_to_remove]] = -float("Inf")
    probs = torch.softmax(logits, dim=-1)
    return torch.multinomial(probs, num_samples=1)
