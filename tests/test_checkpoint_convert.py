import torch

def test_checkpoint_save_load(tmp_path):
    dummy = torch.nn.Linear(4, 4)
    path = tmp_path / "dummy.pt"
    torch.save(dummy.state_dict(), path)
    state = torch.load(path)
    assert "weight" in state
