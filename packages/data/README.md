# Data Directory

Contains all data processing pipelines for the mini-GPT PoC.

## Structure

- `builders/`: Scripts to build datasets from books, code, and web.
- `dataloaders/`: PyTorch dataloaders and collate functions.
- `filters/`: Language, perplexity, and PII filters.
- `sharders/`: Split datasets into shards and pack sequences.
- `preprocessing.py`: Text cleaning utilities.
- `sample_train.jsonl`: Small sample dataset for Free-Tier experiments.

## Usage

```bash
python builders/books_pipeline.py
python builders/code_pipeline.py
python builders/web_pipeline.py
python builders/dedupe.py
python sharders/jsonl_to_mds.py
