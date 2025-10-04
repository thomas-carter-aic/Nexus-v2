"""
Train a simple character-level tokenizer for mini-GPT.
Free-Tier uses small vocab (~256 tokens).
"""

import json
import os

def train_char_tokenizer(dataset_files, vocab_size=256, save_path="./models/tokenizer.json"):
    vocab = set()
    for file in dataset_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                vocab.update(line.strip())
                if len(vocab) >= vocab_size:
                    break
    vocab = sorted(list(vocab))[:vocab_size]
    tokenizer = {ch: i for i, ch in enumerate(vocab)}
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(tokenizer, f)
    print(f"Tokenizer saved to {save_path}")
