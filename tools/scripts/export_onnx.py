"""
Export model to ONNX format (Free-Tier CPU demo)
"""

import torch
from gptx.modules.model import GPTModel

if __name__ == "__main__":
    model = GPTModel(vocab_size=50257, d_model=128, n_layers=2, n_heads=4, max_seq_len=32)
    dummy_input = torch.randint(0, 50257, (1, 32))
    torch.onnx.export(
        model,
        dummy_input,
        "models/mini_gpt.onnx",
        input_names=["input_ids"],
        output_names=["logits"],
        opset_version=13,
    )
    print("Saved mini-GPT ONNX model to models/mini_gpt.onnx")
