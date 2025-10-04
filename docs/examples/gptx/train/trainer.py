"""
Simple training loop for mini-GPT.
Supports Free-Tier batch sizes, gradient accumulation, eval hooks.
"""

import torch
from torch.utils.data import DataLoader
from gptx.optim.fused_adamw import FusedAdamW
from gptx.optim.schedulers import cosine_warmup_scheduler
from gptx.train.loss import CausalLMLoss
from gptx.train.callbacks import CheckpointCallback

class Trainer:
    def __init__(self, model, dataset, vocab_size, lr=1e-4, batch_size=2, device="cpu"):
        self.model = model.to(device)
        self.device = device
        self.dataset = dataset
        self.batch_size = batch_size
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        self.optimizer = FusedAdamW(self.model.parameters(), lr=lr)
        self.scheduler = cosine_warmup_scheduler(self.optimizer, warmup_steps=10, total_steps=100)
        self.criterion = CausalLMLoss()
        self.checkpoint_cb = CheckpointCallback(save_dir="./checkpoints", save_steps=10)

    def train(self, epochs=1):
        self.model.train()
        for epoch in range(epochs):
            for step, batch in enumerate(self.dataloader):
                input_ids = batch["input_ids"].to(self.device)
                labels = input_ids.clone()
                self.optimizer.zero_grad()
                logits = self.model(input_ids)
                loss = self.criterion(logits, labels)
                loss.backward()
                self.optimizer.step()
                self.scheduler.step()
                self.checkpoint_cb.maybe_save(self.model, step)
                if step % 5 == 0:
                    print(f"Epoch {epoch} Step {step} Loss {loss.item():.4f}")
