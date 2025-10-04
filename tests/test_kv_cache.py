import torch
from gptx.modules.attention import KVCache

def test_kv_cache_shapes():
    cache = KVCache(num_heads=2, head_dim=4, seq_len=8)
    k = torch.rand(1, 2, 8, 4)
    v = torch.rand(1, 2, 8, 4)
    cache.update(k, v)
    assert cache.k.shape == (1, 2, 8, 4)
