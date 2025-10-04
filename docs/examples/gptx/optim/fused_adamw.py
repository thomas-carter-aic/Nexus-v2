"""
Fused AdamW optimizer for GPT training.
Supports mixed precision and gradient scaling hooks for Free-Tier or full-scale training.
"""

import torch
from torch.optim import Optimizer

class FusedAdamW(Optimizer):
    """Simplified AdamW optimizer with weight decay and fused step"""
    def __init__(self, params, lr=1e-4, betas=(0.9, 0.95), eps=1e-8, weight_decay=0.01):
        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad
                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p)
                    state['exp_avg_sq'] = torch.zeros_like(p)
                
                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                beta1, beta2 = group['betas']
                state['step'] += 1

                # Update biased moments
                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

                # Bias correction
                bias_correction1 = 1 - beta1 ** state['step']
                bias_correction2 = 1 - beta2 ** state['step']
                denom = (exp_avg_sq.sqrt() / (bias_correction2 ** 0.5)).add_(group['eps'])

                # Weight decay
                p.data.add_(p.data, alpha=-group['lr']*group['weight_decay'])
                # Parameter update
                p.data.addcdiv_(exp_avg, denom, value=-group['lr'])
        return loss
