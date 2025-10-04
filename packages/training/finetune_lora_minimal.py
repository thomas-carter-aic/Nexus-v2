"""
Minimal fine-tune script using HF Trainer + PEFT (for Free-Tier small runs)
Usage:
  python training/finetune_lora_minimal.py --config configs/train_small.yaml --data data/sample_train.jsonl
"""
import argparse, yaml
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/train_small.yaml")
    p.add_argument("--data", default="data/sample_train.jsonl")
    return p.parse_args()

def main():
    args = parse_args()
    cfg = yaml.safe_load(open(args.config))
    model_id = cfg["model"]["hf_id"]
    tok_id = cfg["model"]["tokenizer_id"]

    tokenizer = AutoTokenizer.from_pretrained(tok_id, use_fast=False)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token":"<pad>"})

    # Try load in 8-bit if bitsandbytes available (saves memory); else CPU/GPU normal
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map="auto")
        model.config.use_cache = False
        model = prepare_model_for_kbit_training(model)
    except Exception:
        model = AutoModelForCausalLM.from_pretrained(model_id)
        model.config.use_cache = False

    # Apply LoRA
    lora_cfg = cfg.get("lora", {})
    if lora_cfg.get("enabled", False):
        peft_config = LoraConfig(
            r=lora_cfg.get("r",4),
            lora_alpha=lora_cfg.get("lora_alpha",16),
            target_modules=lora_cfg.get("target_modules", ["q_proj","v_proj","k_proj","o_proj"]),
            bias="none",
            task_type="CAUSAL_LM"
        )
        model = get_peft_model(model, peft_config)

    ds = load_dataset("json", data_files={"train": args.data})["train"]
    max_length = cfg["train"]["max_length"]

    def tokenize_fn(batch):
        return tokenizer(batch["text"], truncation=True, max_length=max_length)

    ds = ds.map(tokenize_fn, batched=True, remove_columns=["text"])
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    ta = cfg["train"]
    training_args = TrainingArguments(
        output_dir=ta["output_dir"],
        per_device_train_batch_size=ta["per_device_train_batch_size"],
        gradient_accumulation_steps=ta["gradient_accumulation_steps"],
        num_train_epochs=ta["num_train_epochs"],
        logging_steps=ta["logging_steps"],
        save_strategy="steps",
        save_steps=ta["save_steps"],
        save_total_limit=ta["save_total_limit"],
        learning_rate=ta["learning_rate"],
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds,
        data_collator=collator
    )

    trainer.train()
    model.save_pretrained(ta["output_dir"])
    tokenizer.save_pretrained(ta["output_dir"])
    print("Saved model to", ta["output_dir"])

if __name__ == "__main__":
    main()
