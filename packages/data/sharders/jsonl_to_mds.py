"""
Shard JSONL into multiple smaller JSONL files for Free-Tier training.
"""

import json
from pathlib import Path

def shard_jsonl(input_path: str, output_dir: str, shard_size: int = 100):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    shard = []
    shard_idx = 0

    with open(input_path, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f):
            shard.append(json.loads(line))
            if (line_idx + 1) % shard_size == 0:
                shard_file = output_dir / f"shard_{shard_idx}.jsonl"
                with open(shard_file, "w", encoding="utf-8") as out:
                    for entry in shard:
                        out.write(json.dumps(entry) + "\n")
                shard = []
                shard_idx += 1

    # write remaining
    if shard:
        shard_file = output_dir / f"shard_{shard_idx}.jsonl"
        with open(shard_file, "w", encoding="utf-8") as out:
            for entry in shard:
                out.write(json.dumps(entry) + "\n")
