"""
Load and apply SentencePiece tokenizer
"""

import sentencepiece as spm

sp = spm.SentencePieceProcessor()
sp.Load("tokenizers/spm_model.model")

def encode(text):
    return sp.EncodeAsIds(text)

def decode(ids):
    return sp.DecodeIds(ids)
