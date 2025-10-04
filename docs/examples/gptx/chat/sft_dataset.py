"""
Supervised Fine-Tuning (SFT) dataset
"""

from torch.utils.data import Dataset

class SFTDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return {"input_ids": self.data[idx]["input_ids"]}
