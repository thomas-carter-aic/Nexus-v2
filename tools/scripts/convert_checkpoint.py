"""
Convert trained PyTorch checkpoint to deployable format (e.g., ONNX or TorchScript)
"""

import torch
from gptx.modules.model import GPTModel

def convert_to_torchscript(model_path, save_path):
    model = GPTModel(vocab_size=50257, d_model=128, n_layers=2, n_heads=4, max_seq_len=128)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    scripted = torch.jit.script(model)
    torch.jit.save(scripted, save_path)
    print(f"Checkpoint converted to TorchScript at {save_path}")
