"""
Books dataset pipeline builder.
Loads and processes book text datasets for LM training.
"""

import json
from pathlib import Path

def build_books_dataset(input_dir: str, output_path: str, max_lines: int = 1000):
    """
    Reads book text files, cleans, and writes to JSONL.
    
    Args:
        input_dir (str): Directory with raw book text files.
        output_path (str): Path to save processed JSONL.
        max_lines (int): Number of lines per file to process (for Free-Tier PoC).
    """
    input_path = Path(input_dir)
    output_file = Path(output_path)
    
    data = []
    for file in input_path.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                line = line.strip()
                if line:
                    data.append({"text": line})
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as out:
        for entry in data:
            out.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    build_books_dataset("data/raw/books", "data/sample_train.jsonl")
