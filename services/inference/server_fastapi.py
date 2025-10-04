# Minimal FastAPI server to serve the small model (cpu or gpu)
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import yaml
import torch

app = FastAPI()

class GenRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 64
    temperature: float = 0.7
    top_p: float = 0.9

# load config
cfg = yaml.safe_load(open("configs/inference.yaml"))
model_path = cfg["server"]["model_path"]
device = cfg["server"]["device"]

print("Loading model:", model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_path)
model.to(device if device=="cpu" else "cuda")
model.eval()

@app.post("/generate")
def generate(req: GenRequest):
    inputs = tokenizer(req.prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k,v in inputs.items()}
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=req.max_new_tokens, temperature=req.temperature, top_p=req.top_p)
    txt = tokenizer.decode(out[0], skip_special_tokens=True)
    return {"text": txt}
