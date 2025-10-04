"""
FastAPI server for serving GPT predictions.
Free-Tier demo supports single GPU or CPU inference.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import torch

from gptx.modules.model import GPTModel
from gptx.train.trainer import Trainer

app = FastAPI()

# Example mini GPT model
vocab_size = 50257
model = GPTModel(vocab_size=vocab_size, d_model=128, n_layers=2, n_heads=4, max_seq_len=128)
model.eval()

class PredictRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 32

@app.post("/predict")
def predict(req: PredictRequest):
    # Simple tokenization: char-level
    input_ids = torch.tensor([[ord(c) % vocab_size for c in req.prompt]], dtype=torch.long)
    with torch.no_grad():
        logits = model(input_ids)
        # greedy sampling
        next_token = torch.argmax(logits[:, -1, :], dim=-1)
    return {"next_token_id": next_token.item()}
