import torch
from gptx.modules.block import GPTBlock

def test_block_forward():
    block = GPTBlock(d_model=16, n_heads=2)
    x = torch.rand(1, 8, 16)
    y = block(x)
    assert y.shape == x.shape
