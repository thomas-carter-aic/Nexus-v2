"""
Merge LoRA adapters into base model (Free-Tier demo placeholder)
"""

import torch

def merge_lora(base_model, lora_weights):
    """
    Simple merge: add LoRA weights to base model weights
    """
    for name, param in base_model.named_parameters():
        if name in lora_weights:
            param.data += lora_weights[name]
    return base_model

if __name__ == "__main__":
    print("LoRA merge demo (Free-Tier placeholder)")
