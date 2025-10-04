"""
Evaluate model performance on long context sequences
"""

from gptx.modules.model import GPTModel
import torch

def long_context_eval(model, seq_len=128):
    input_ids = torch.randint(0, 50257, (1, seq_len))
    model.eval()
    with torch.no_grad():
        logits = model(input_ids)
    return logits.shape
