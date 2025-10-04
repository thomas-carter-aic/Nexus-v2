"""
Memory utilities for GPT models.

Provides:
- Parameter count and memory estimation
- Device-aware usage reporting
- Lightweight profiling hooks
"""

import torch

def count_parameters(model):
    """
    Count total number of parameters in the model.
    
    Args:
        model: torch.nn.Module
    
    Returns:
        total_params (int): Total number of parameters
    """
    return sum(p.numel() for p in model.parameters())

def estimate_memory(model, dtype=torch.float32):
    """
    Estimate memory footprint of the model in MB.

    Args:
        model: torch.nn.Module
        dtype: torch dtype (default float32)
    
    Returns:
        mem_mb (float): Approximate memory in MB
    """
    total_params = count_parameters(model)
    bytes_per_param = torch.tensor([], dtype=dtype).element_size()
    mem_bytes = total_params * bytes_per_param
    mem_mb = mem_bytes / 1024**2
    return mem_mb

def device_memory_report(model=None):
    """
    Report device memory usage.
    Works on both CPU and GPU.
    
    Args:
        model: optional torch.nn.Module to estimate params
    
    Returns:
        report (dict): memory stats in MB
    """
    report = {}
    if torch.cuda.is_available():
        report["cuda_total_MB"] = torch.cuda.get_device_properties(0).total_memory / 1024**2
        report["cuda_reserved_MB"] = torch.cuda.memory_reserved(0) / 1024**2
        report["cuda_allocated_MB"] = torch.cuda.memory_allocated(0) / 1024**2
    else:
        import psutil
        report["cpu_total_MB"] = psutil.virtual_memory().total / 1024**2
        report["cpu_used_MB"] = psutil.virtual_memory().used / 1024**2

    if model is not None:
        report["model_params_MB"] = estimate_memory(model)
    
    return report

def print_memory_report(model=None):
    """
    Pretty-print memory report.
    """
    report = device_memory_report(model)
    print("=== Memory Report ===")
    for k, v in report.items():
        print(f"{k}: {v:.2f} MB")
    print("====================")
