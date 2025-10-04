"""
Collate function for language model training.
Prepares batches with padding and optional attention masks.
"""

from typing import List
import torch

def collate_lm(batch: List[dict], pad_token_id: int = 0, device: str = "cpu"):
    """
    Args:
        batch: List of dicts with "input_ids"
        pad_token_id: token id used for padding
        device: "cpu" or "cuda"

    Returns:
        dict with tensors: input_ids, attention_mask
    """
    input_ids_list = [torch.tensor(item["input_ids"], dtype=torch.long) for item in batch]
    max_len = max(len(ids) for ids in input_ids_list)
    padded_ids = []

    for ids in input_ids_list:
        pad_len = max_len - len(ids)
        padded = torch.cat([ids, torch.full((pad_len,), pad_token_id, dtype=torch.long)])
        padded_ids.append(padded)

    input_ids_tensor = torch.stack(padded_ids).to(device)
    attention_mask = (input_ids_tensor != pad_token_id).long()

    return {"input_ids": input_ids_tensor, "attention_mask": attention_mask}
