import torch
from gptx.utils.sampling import greedy_sample

def test_greedy_sample():
    logits = torch.tensor([[1.0, 2.0, 3.0]])
    token = greedy_sample(logits)
    assert token.item() == 2
