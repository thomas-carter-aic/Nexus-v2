"""
Code dataset pipeline builder.
Processes code snippets for LM pretraining (Python/JS etc.)
"""

import json
from pathlib import Path

def build_code_dataset(input_dir: str, output_path: str, max_snippets: int = 500):
    """
    Args:
        input_dir: raw code files
        output_path: JSONL output
        max_snippets: limit for Free-Tier PoC
    """
    input_path = Path(input_dir)
    output_file = Path(output_path)
    data = []

    for file in input_path.glob("**/*.py"):
        with open(file, "r", encoding="utf-8") as f:
            snippet = f.read().strip()
            if snippet:
                data.append({"text": snippet})
        if len(data) >= max_snippets:
            break

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as out:
        for entry in data:
            out.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    build_code_dataset("data/raw/code", "data/sample_train.jsonl")
