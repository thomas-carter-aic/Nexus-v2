"""
AWS Lambda handler for serverless inference.
Free-Tier demo works with small GPT models.
"""

import json
import torch
from gptx.modules.model import GPTModel

vocab_size = 50257
model = GPTModel(vocab_size=vocab_size, d_model=128, n_layers=2, n_heads=4, max_seq_len=128)
model.eval()

def lambda_handler(event, context):
    prompt = event.get("prompt", "")
    input_ids = torch.tensor([[ord(c) % vocab_size for c in prompt]], dtype=torch.long)
    with torch.no_grad():
        logits = model(input_ids)
        next_token = torch.argmax(logits[:, -1, :], dim=-1)
    return {
        "statusCode": 200,
        "body": json.dumps({"next_token_id": next_token.item()})
    }
