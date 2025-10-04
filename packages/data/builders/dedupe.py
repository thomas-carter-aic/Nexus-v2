"""
Simple deduplication script for JSONL datasets.
"""

import json

def dedupe_jsonl(input_path: str, output_path: str):
    seen_texts = set()
    output_data = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            text = obj["text"]
            if text not in seen_texts:
                seen_texts.add(text)
                output_data.append(obj)

    with open(output_path, "w", encoding="utf-8") as out:
        for entry in output_data:
            out.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    dedupe_jsonl("data/sample_train.jsonl", "data/sample_train_dedup.jsonl")
