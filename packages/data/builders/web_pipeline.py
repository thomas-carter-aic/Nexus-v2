"""
Web text pipeline builder.
Fetches, cleans, and tokenizes web-scraped text for LM pretraining.
"""

import json
from pathlib import Path

def build_web_dataset(input_dir: str, output_path: str, max_pages: int = 200):
    input_path = Path(input_dir)
    output_file = Path(output_path)
    data = []

    for file in input_path.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                data.append({"text": text})
        if len(data) >= max_pages:
            break

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as out:
        for entry in data:
            out.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    build_web_dataset("data/raw/web", "data/sample_train.jsonl")
