"""
Checkpoint utilities.
Supports saving/loading model, optimizer, and scheduler states.
"""

import torch

def save_checkpoint(model, optimizer, scheduler, path):
    state = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "scheduler": scheduler.state_dict()
    }
    torch.save(state, path)

def load_checkpoint(model, optimizer, scheduler, path):
    state = torch.load(path)
    model.load_state_dict(state["model"])
    optimizer.load_state_dict(state["optimizer"])
    scheduler.load_state_dict(state["scheduler"])
