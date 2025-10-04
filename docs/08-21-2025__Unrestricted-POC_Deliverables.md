# ✅ Deliverables

## 1. **Repository Structure (`aic-ai-poc-gpt/`)**

A **modular, production-structured repo** for an AI-native GPT-style model, with clean separation of concerns:

```
aic-ai-poc-gpt/
│
├── gptx/                   # Core GPT implementation
│   ├── layers/             # Transformer building blocks
│   ├── utils/              # Shared utilities (KV cache, memory mgmt, sampling, etc.)
│   ├── configs/            # Model configs (GPT2, TinyLLaMA, custom)
│   └── __init__.py
│
├── models/                 # Predefined model families
│   ├── adapters/           # Adapter layers for fine-tuning
│   ├── gpt2_small/         # Small GPT-2 variant (fast to train/test)
│   ├── tinyllama/          # TinyLLaMA variant (modern efficient baseline)
│
├── training/               # Training orchestration
│   ├── utils.py            # Training helpers (logging, gradient scaling, etc.)
│   ├── train.py            # Main training loop entrypoint
│
├── tokenizers/             # Tokenizer handling
│   ├── utils.py
│   ├── train_spm.py        # SentencePiece tokenizer trainer
│   ├── spm_model.py        # SentencePiece model wrapper
│
├── tests/                  # Unit tests for correctness
│   ├── test_sampler.py
│   ├── test_rope_alibi.py
│   ├── test_kv_cache.py
│   ├── test_checkpoint_convert.py
│   ├── test_block_shapes.py
│
└── README.md               # Documentation
```

---

## 2. **Minimal PoC (AWS Free Tier / <\$50 per month)**

We built a **baseline branch** that:

* Runs on **AWS Free Tier** (EC2 micro, S3, EBS, etc.) with cost-awareness.
* Uses **TinyLLaMA + GPT-2 small configs** for quick prototyping.
* Includes **training, evaluation, and tokenizer pipelines**.
* Has **KV cache + memory utils** for inference efficiency.
* Provides **unit tests** for model correctness and reproducibility.

This gives you a **bootstrapped, end-to-end workflow**:

1. Train tokenizer (SentencePiece).
2. Train model (small GPT variant).
3. Save/load checkpoints.
4. Run inference with memory-efficient attention.
5. Validate correctness with unit tests.

---

## 3. **Next Branch (No Budget Limitations)**

A **new branch** that removes cost limits:

* Support for **larger models** (13B, 34B, etc.).
* **Multi-GPU + distributed training** (DeepSpeed, FSDP, Megatron-LM style sharding).
* Advanced **data pipelines** (streaming from large corpora).
* **Better optimizers** (AdamW, Lion, Sophia).
* **Full observability stack** (TensorBoard, WandB, Prometheus+Grafana).
* Cloud scalability (AWS, GCP, Azure, on-prem hybrid).

This turns the repo into a **real LLM development platform**, not just a PoC.

---

## 4. **Practical Outcomes**

* **Bootstrap a tokenizer + model from scratch** (GPT2-small / TinyLLaMA scale).
* **Train + eval on AWS free tier**.
* **Run inference with KV cache** (fast autoregressive generation).
* **Validate correctness with tests** (ensuring reliability).
* **Extend easily**: you have a modular repo that can grow into enterprise-scale R\&D.

---

Sumamry:
A **full GPT PoC stack**, lean enough for **free-tier AWS**, but with the repo already structured to scale up into a **production-grade LLM platform** once you switch branches and lift the budget constraints.