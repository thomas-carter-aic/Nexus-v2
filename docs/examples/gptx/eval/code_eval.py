"""
Evaluate code generation capability
"""

from gptx.modules.model import GPTModel
import torch

def code_eval(model, test_inputs):
    results = []
    model.eval()
    with torch.no_grad():
        for inp in test_inputs:
            input_ids = torch.tensor([inp])
            logits = model(input_ids)
            next_token = torch.argmax(logits[:, -1, :], dim=-1)
            results.append(next_token.item())
    return results
