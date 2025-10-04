"""
Mini-DS (MDS) dataset loader for PoC.
Supports streaming from sharded binary format or JSONL.
"""

import json
from pathlib import Path
from typing import Iterator, Dict

def load_jsonl(path: str, max_samples: int = 1000) -> Iterator[Dict]:
    """
    Generator yielding dicts from JSONL
    """
    path = Path(path)
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)
            count += 1
            if count >= max_samples:
                break
