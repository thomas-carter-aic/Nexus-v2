"""
Tokenizer utilities
"""

def detokenize(ids):
    return ''.join([chr(i % 256) for i in ids])

def batch_detokenize(batch_ids):
    return [detokenize(ids) for ids in batch_ids]
