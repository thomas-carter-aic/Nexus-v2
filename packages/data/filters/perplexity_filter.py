"""
Perplexity-based filter to remove low-quality text.
Uses HuggingFace small LM for PoC.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
model.eval()

def filter_perplexity(text: str, threshold: float = 50.0):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        loss = model(**inputs, labels=inputs["input_ids"]).loss
        ppl = torch.exp(loss)
    return ppl < threshold
