import torch
from gptx.utils.rope_scaling import apply_rope

def test_rope_shape():
    x = torch.rand(1, 4, 16)
    y = apply_rope(x)
    assert y.shape == x.shape
