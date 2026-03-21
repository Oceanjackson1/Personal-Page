---
title: "Fine Tuning Expert"
description: "Use when fine-tuning LLMs, training custom models, or adapting foundation models for specific tasks. Invoke for configuring LoRA/QLoRA adapters, preparing JSONL training datasets, setting hyperparameters for fine-tuning runs, adapter training, tra..."
category: "research"
source: "community"
author: "Community"
tags: ["fine", "tuning"]
date: 2026-03-20
---

# Fine-Tuning Expert

Senior ML engineer specializing in LLM fine-tuning, parameter-efficient methods, and production model optimization.

## Core Workflow

1. **Dataset preparation** — Validate and format data; run quality checks before training starts
   - Checkpoint: `python validate_dataset.py --input data.jsonl` — fix all errors before proceeding
2. **Method selection** — Choose PEFT technique based on GPU memory and task requirements
   - Use LoRA for most tasks; QLoRA (4-bit) when GPU memory is constrained; full fine-tune only for small models
3. **Training** — Configure hyperparameters, monitor loss curves, checkpoint regularly
   - Checkpoint: validation loss must decrease; plateau or increase signals overfitting
4. **Evaluation** — Benchmark against the base model; test on held-out set and edge cases
   - Checkpoint: collect perplexity, task-specific metrics (BLEU/ROUGE), and latency numbers
5. **Deployment** — Merge adapter weights, quantize, measure inference throughput before serving

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| LoRA/PEFT | `references/lora-peft.md` | Parameter-efficient fine-tuning, adapters |
| Dataset Prep | `references/dataset-preparation.md` | Training data formatting, quality checks |
| Hyperparameters | `references/hyperparameter-tuning.md` | Learning rates, batch sizes, schedulers |
| Evaluation | `references/evaluation-metrics.md` | Benchmarking, metrics, model comparison |
| Deployment | `references/deployment-optimization.md` | Model merging, quantization, serving |

## Minimal Working Example — LoRA Fine-Tuning with Hugging Face PEFT

```python
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
import torch

# 1. Load base model and tokenizer
model_id = "meta-llama/Llama-3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# 2. Configure LoRA adapter
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,               # rank — increase for more capacity, decrease to save memory
    lora_alpha=32,      # scaling factor; typically 2× rank
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # verify: should be ~0.1–1% of total params

# 3. Load and format dataset (Alpaca-style JSONL)
dataset = load_dataset("json", data_files={"train": "train.jsonl", "test": "test.jsonl"})

def format_prompt(example):
    return {"text": f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"}

dataset = dataset.map(format_prompt)

# 4. Training arguments
training_args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,     # effective batch size = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,                 # always use warmup
    fp16=False,
    bf16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=100,
    save_steps=200,
    load_best_model_at_end=True,
)

# 5. Train
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    dataset_text_field="text",
    max_seq_length=2048,
)
trainer.train()

# 6. Save adapter weights only
model.save_pretrained("./lora-adapter")
tokenizer.save_pretrained("./lora-adapter")
```

**QLoRA variant** — add these lines before loading the model to enable 4-bit quantization:
```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
```

**Merge adapter into base model for deployment:**
```python
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
merged = PeftModel.from_pretrained(base, "./lora-adapter").merge_and_unload()
merged.save_pretrained("./merged-model")
```

## Constraints

### MUST DO
- Validate dataset quality before training
- Use parameter-efficient methods for large models (>7B)
- Monitor training/validation loss curves
- Document hyperparameters and training config
- Version datasets and model checkpoints
- Always include a learning rate warmup

### MUST NOT DO
- Skip data quality validation
- Overfit on small datasets — use regularisation (dropout, weight decay) and early stopping
- Merge incompatible adapters (mismatched rank, base model, or target modules)
- Deploy without evaluation against a held-out set and latency benchmark

## Output Templates

When implementing fine-tuning, always provide:
1. **Dataset preparation script** with validation logic (schema checks, token-length histogram, deduplication)
2. **Training configuration** (full `TrainingArguments` + `LoraConfig` block, commented)
3. **Evaluation script** reporting perplexity, task-specific metrics, and latency
4. **Brief design rationale** — why this PEFT method, rank, and learning rate were chosen for this task

---

## Reference: Dataset Preparation

# Dataset Preparation for Fine-Tuning

---

## Overview

Dataset quality is the most important factor in fine-tuning success. This reference covers data formatting, validation, cleaning, and best practices for creating high-quality training data.

## Dataset Formats

### Alpaca Format (Instruction-Response)

```python
# Single-turn instruction format
alpaca_example = {
    "instruction": "Summarize the following article in 2-3 sentences.",
    "input": "The article text goes here...",
    "output": "The summary goes here."
}

# Without input field
alpaca_no_input = {
    "instruction": "What are the three primary colors?",
    "input": "",
    "output": "The three primary colors are red, blue, and yellow."
}
```

### ShareGPT Format (Multi-Turn Conversations)

```python
# Multi-turn conversation format
sharegpt_example = {
    "conversations": [
        {"from": "human", "value": "What is machine learning?"},
        {"from": "gpt", "value": "Machine learning is a subset of AI that enables..."},
        {"from": "human", "value": "Can you give me an example?"},
        {"from": "gpt", "value": "A common example is email spam filtering..."}
    ]
}

# Alternative format with roles
openai_format = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"},
        {"role": "assistant", "content": "Machine learning is..."}
    ]
}
```

### Converting Between Formats

```python
from typing import TypedDict
from datasets import Dataset

class AlpacaExample(TypedDict):
    instruction: str
    input: str
    output: str

class ShareGPTExample(TypedDict):
    conversations: list[dict[str, str]]

def alpaca_to_sharegpt(example: AlpacaExample) -> ShareGPTExample:
    """Convert Alpaca format to ShareGPT multi-turn format."""
    user_content = example["instruction"]
    if example.get("input"):
        user_content += f"\n\n{example['input']}"

    return {
        "conversations": [
            {"from": "human", "value": user_content},
            {"from": "gpt", "value": example["output"]}
        ]
    }

def sharegpt_to_messages(example: ShareGPTExample, system_prompt: str = "") -> dict:
    """Convert ShareGPT to OpenAI messages format."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    role_map = {"human": "user", "gpt": "assistant", "system": "system"}
    for turn in example["conversations"]:
        messages.append({
            "role": role_map.get(turn["from"], turn["from"]),
            "content": turn["value"]
        })

    return {"messages": messages}
```

## Formatting for Training

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

def format_instruction_prompt(
    instruction: str,
    input_text: str = "",
    response: str = "",
    system_prompt: str = "You are a helpful assistant."
) -> str:
    """Format for Llama 3.1 Instruct chat template."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{instruction}\n{input_text}".strip()},
    ]
    if response:
        messages.append({"role": "assistant", "content": response})

    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=not response  # Add prompt if no response
    )

# Example usage
formatted = format_instruction_prompt(
    instruction="Translate to French:",
    input_text="Hello, how are you?",
    response="Bonjour, comment allez-vous?"
)
```

## Dataset Validation

```python
from dataclasses import dataclass
from collections import Counter
import re

@dataclass
class DatasetStats:
    total_examples: int
    avg_input_length: float
    avg_output_length: float
    max_input_length: int
    max_output_length: int
    empty_inputs: int
    empty_outputs: int
    duplicate_count: int
    language_distribution: dict

def validate_dataset(examples: list[dict], tokenizer) -> tuple[DatasetStats, list[str]]:
    """
    Validate dataset and return statistics and warnings.

    Args:
        examples: List of training examples
        tokenizer: Tokenizer for length calculations

    Returns:
        Tuple of (stats, warnings)
    """
    warnings = []
    input_lengths = []
    output_lengths = []
    seen_inputs = set()
    duplicates = 0

    for i, ex in enumerate(examples):
        # Check for required fields
        if "instruction" not in ex and "messages" not in ex:
            warnings.append(f"Example {i}: Missing instruction or messages field")
            continue

        # Get input/output text
        if "instruction" in ex:
            input_text = f"{ex.get('instruction', '')} {ex.get('input', '')}".strip()
            output_text = ex.get("output", "")
        else:
            input_text = " ".join(m["content"] for m in ex["messages"] if m["role"] == "user")
            output_text = " ".join(m["content"] for m in ex["messages"] if m["role"] == "assistant")

        # Check for empty fields
        if not input_text:
            warnings.append(f"Example {i}: Empty input")
        if not output_text:
            warnings.append(f"Example {i}: Empty output")

        # Check lengths
        input_len = len(tokenizer.encode(input_text))
        output_len = len(tokenizer.encode(output_text))
        input_lengths.append(input_len)
        output_lengths.append(output_len)

        if input_len + output_len > 4096:
            warnings.append(f"Example {i}: Total length {input_len + output_len} exceeds 4096")

        # Check for duplicates
        input_hash = hash(input_text)
        if input_hash in seen_inputs:
            duplicates += 1
        seen_inputs.add(input_hash)

    stats = DatasetStats(
        total_examples=len(examples),
        avg_input_length=sum(input_lengths) / len(input_lengths) if input_lengths else 0,
        avg_output_length=sum(output_lengths) / len(output_lengths) if output_lengths else 0,
        max_input_length=max(input_lengths) if input_lengths else 0,
        max_output_length=max(output_lengths) if output_lengths else 0,
        empty_inputs=sum(1 for w in warnings if "Empty input" in w),
        empty_outputs=sum(1 for w in warnings if "Empty output" in w),
        duplicate_count=duplicates,
        language_distribution={}  # Implement language detection if needed
    )

    return stats, warnings
```

## Data Quality Checks

```python
import re
from typing import Callable

def create_quality_filter(
    min_input_tokens: int = 10,
    max_input_tokens: int = 2048,
    min_output_tokens: int = 5,
    max_output_tokens: int = 2048,
    custom_filters: list[Callable[[dict], bool]] = None
) -> Callable[[dict, AutoTokenizer], bool]:
    """
    Create a quality filter function for dataset examples.

    Returns True if example passes all quality checks.
    """
    def quality_filter(example: dict, tokenizer) -> bool:
        if "instruction" in example:
            input_text = f"{example.get('instruction', '')} {example.get('input', '')}".strip()
            output_text = example.get("output", "")
        else:
            input_text = " ".join(m["content"] for m in example.get("messages", []) if m["role"] == "user")
            output_text = " ".join(m["content"] for m in example.get("messages", []) if m["role"] == "assistant")

        # Length checks
        input_tokens = len(tokenizer.encode(input_text))
        output_tokens = len(tokenizer.encode(output_text))

        if not (min_input_tokens <= input_tokens <= max_input_tokens):
            return False
        if not (min_output_tokens <= output_tokens <= max_output_tokens):
            return False

        # Quality checks
        if not output_text.strip():
            return False

        # Check for common issues
        bad_patterns = [
            r"I cannot",
            r"I'm sorry, but",
            r"As an AI",
            r"I don't have access",
            r"\[.*\]$",  # Trailing brackets
        ]
        for pattern in bad_patterns:
            if re.search(pattern, output_text, re.IGNORECASE):
                return False

        # Custom filters
        if custom_filters:
            for filter_fn in custom_filters:
                if not filter_fn(example):
                    return False

        return True

    return quality_filter

# Usage
quality_filter = create_quality_filter(min_output_tokens=20)
filtered_dataset = [ex for ex in dataset if quality_filter(ex, tokenizer)]
```

## Deduplication

```python
from datasketch import MinHash, MinHashLSH
import hashlib

def exact_dedup(examples: list[dict], key_field: str = "instruction") -> list[dict]:
    """Remove exact duplicates based on a key field."""
    seen = set()
    unique = []
    for ex in examples:
        key = ex.get(key_field, "")
        if key not in seen:
            seen.add(key)
            unique.append(ex)
    return unique

def fuzzy_dedup(
    examples: list[dict],
    key_field: str = "output",
    threshold: float = 0.8,
    num_perm: int = 128
) -> list[dict]:
    """
    Remove near-duplicate examples using MinHash LSH.

    Args:
        examples: List of examples
        key_field: Field to check for similarity
        threshold: Jaccard similarity threshold (0-1)
        num_perm: Number of permutations for MinHash
    """
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    unique = []

    for i, ex in enumerate(examples):
        text = ex.get(key_field, "")
        words = text.lower().split()

        # Create MinHash
        m = MinHash(num_perm=num_perm)
        for word in words:
            m.update(word.encode('utf-8'))

        # Check for near-duplicates
        result = lsh.query(m)
        if not result:
            lsh.insert(str(i), m)
            unique.append(ex)

    return unique

# Combined deduplication pipeline
def deduplicate_dataset(examples: list[dict]) -> list[dict]:
    """Full deduplication pipeline."""
    print(f"Starting examples: {len(examples)}")

    # Step 1: Exact deduplication on input
    examples = exact_dedup(examples, key_field="instruction")
    print(f"After exact dedup on instruction: {len(examples)}")

    # Step 2: Fuzzy deduplication on output
    examples = fuzzy_dedup(examples, key_field="output", threshold=0.85)
    print(f"After fuzzy dedup on output: {len(examples)}")

    return examples
```

## Train/Validation Split

```python
from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
import random

def create_stratified_split(
    examples: list[dict],
    test_size: float = 0.1,
    stratify_field: str = None,
    seed: int = 42
) -> DatasetDict:
    """
    Create train/validation split with optional stratification.

    Args:
        examples: List of examples
        test_size: Fraction for validation set
        stratify_field: Field to stratify by (e.g., "category")
        seed: Random seed for reproducibility
    """
    if stratify_field and all(stratify_field in ex for ex in examples):
        stratify = [ex[stratify_field] for ex in examples]
        train_examples, val_examples = train_test_split(
            examples,
            test_size=test_size,
            stratify=stratify,
            random_state=seed
        )
    else:
        random.seed(seed)
        shuffled = examples.copy()
        random.shuffle(shuffled)
        split_idx = int(len(shuffled) * (1 - test_size))
        train_examples = shuffled[:split_idx]
        val_examples = shuffled[split_idx:]

    return DatasetDict({
        "train": Dataset.from_list(train_examples),
        "validation": Dataset.from_list(val_examples)
    })
```

## Data Augmentation

```python
import random

def augment_instruction(example: dict) -> list[dict]:
    """Generate augmented versions of an instruction example."""
    augmented = [example]

    instruction = example.get("instruction", "")
    input_text = example.get("input", "")
    output = example.get("output", "")

    # Instruction paraphrasing templates
    prefixes = [
        "",
        "Please ",
        "Can you ",
        "I need you to ",
        "Your task is to ",
    ]
    suffixes = [
        "",
        " Be concise.",
        " Provide a detailed response.",
        " Think step by step.",
    ]

    # Generate variations
    for prefix in random.sample(prefixes, min(2, len(prefixes))):
        for suffix in random.sample(suffixes, min(2, len(suffixes))):
            new_instruction = f"{prefix}{instruction[0].lower() if prefix else instruction[0]}{instruction[1:]}{suffix}"
            if new_instruction != instruction:
                augmented.append({
                    "instruction": new_instruction.strip(),
                    "input": input_text,
                    "output": output
                })

    return augmented

def augment_dataset(examples: list[dict], augmentation_factor: float = 1.5) -> list[dict]:
    """
    Augment dataset to reach target size.

    Args:
        examples: Original examples
        augmentation_factor: Target size as multiple of original
    """
    augmented = []
    target_size = int(len(examples) * augmentation_factor)

    for ex in examples:
        variations = augment_instruction(ex)
        augmented.extend(variations)

    # Deduplicate and trim to target
    augmented = exact_dedup(augmented, "instruction")
    random.shuffle(augmented)
    return augmented[:target_size]
```

## Loading and Saving Datasets

```python
from datasets import load_dataset, Dataset
import json

def load_custom_dataset(path: str) -> Dataset:
    """Load dataset from various formats."""
    if path.endswith(".jsonl"):
        return load_dataset("json", data_files=path, split="train")
    elif path.endswith(".json"):
        with open(path, "r") as f:
            data = json.load(f)
        return Dataset.from_list(data)
    elif path.endswith(".parquet"):
        return load_dataset("parquet", data_files=path, split="train")
    else:
        # Try loading from Hugging Face Hub
        return load_dataset(path, split="train")

def save_dataset(dataset: Dataset, path: str, format: str = "jsonl"):
    """Save dataset in specified format."""
    if format == "jsonl":
        dataset.to_json(path, orient="records", lines=True)
    elif format == "parquet":
        dataset.to_parquet(path)
    elif format == "json":
        with open(path, "w") as f:
            json.dump(list(dataset), f, indent=2)
```

## Dataset Size Guidelines

| Task Type | Minimum Examples | Recommended | Notes |
|-----------|------------------|-------------|-------|
| Classification | 100 per class | 500+ per class | Balance classes |
| Instruction Following | 1,000 | 5,000-10,000 | Diverse instructions |
| Domain Adaptation | 5,000 | 20,000+ | High-quality domain data |
| Code Generation | 2,000 | 10,000+ | Include edge cases |
| Multi-turn Chat | 1,000 conversations | 5,000+ | Varied conversation lengths |

## Quick Reference

```python
# Complete dataset preparation pipeline
from datasets import Dataset

def prepare_dataset(raw_data_path: str, output_path: str, tokenizer) -> Dataset:
    """Full dataset preparation pipeline."""
    # 1. Load raw data
    examples = load_custom_dataset(raw_data_path)

    # 2. Validate
    stats, warnings = validate_dataset(list(examples), tokenizer)
    print(f"Dataset stats: {stats}")
    if warnings[:10]:  # Show first 10 warnings
        print(f"Sample warnings: {warnings[:10]}")

    # 3. Filter for quality
    quality_filter = create_quality_filter()
    examples = [ex for ex in examples if quality_filter(ex, tokenizer)]
    print(f"After quality filter: {len(examples)}")

    # 4. Deduplicate
    examples = deduplicate_dataset(examples)
    print(f"After deduplication: {len(examples)}")

    # 5. Split
    dataset = create_stratified_split(examples, test_size=0.1)

    # 6. Save
    dataset["train"].to_json(f"{output_path}/train.jsonl", lines=True)
    dataset["validation"].to_json(f"{output_path}/val.jsonl", lines=True)

    return dataset

# Usage
dataset = prepare_dataset("raw_data.jsonl", "./processed", tokenizer)
```

## Related References

- `lora-peft.md` - Training configuration
- `evaluation-metrics.md` - Measuring dataset quality impact
- `hyperparameter-tuning.md` - Adjusting training for dataset size

---

## Reference: Deployment Optimization

# Deployment and Optimization for Fine-Tuned Models

---

## Overview

Deploying fine-tuned models efficiently requires adapter merging, quantization, and inference optimization. This reference covers techniques to minimize latency and memory while maintaining quality.

## Adapter Merging

### Merging LoRA Adapters

```python
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def merge_lora_adapter(
    base_model_name: str,
    adapter_path: str,
    output_path: str,
    push_to_hub: bool = False,
    hub_repo: str = None
):
    """
    Merge LoRA adapter into base model and save.

    This creates a standalone model without adapter overhead.
    """
    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )

    # Load adapter
    model = PeftModel.from_pretrained(base_model, adapter_path)

    # Merge adapter weights into base model
    print("Merging adapter weights...")
    merged_model = model.merge_and_unload()

    # Save merged model
    print(f"Saving merged model to {output_path}")
    merged_model.save_pretrained(output_path)

    # Save tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    tokenizer.save_pretrained(output_path)

    if push_to_hub and hub_repo:
        print(f"Pushing to hub: {hub_repo}")
        merged_model.push_to_hub(hub_repo)
        tokenizer.push_to_hub(hub_repo)

    return merged_model

# Usage
# merge_lora_adapter(
#     "meta-llama/Llama-3.1-8B",
#     "./lora-adapter",
#     "./merged-model"
# )
```

### Merging Multiple Adapters

```python
from peft import PeftModel

def merge_multiple_adapters(
    base_model_name: str,
    adapters: dict[str, float],
    output_path: str
):
    """
    Merge multiple LoRA adapters with weighted combination.

    Args:
        base_model_name: Base model name or path
        adapters: Dict of {adapter_path: weight}
        output_path: Output path for merged model
    """
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    # Load first adapter
    adapter_paths = list(adapters.keys())
    model = PeftModel.from_pretrained(
        base_model,
        adapter_paths[0],
        adapter_name="adapter_0"
    )

    # Load remaining adapters
    for i, adapter_path in enumerate(adapter_paths[1:], 1):
        model.load_adapter(adapter_path, adapter_name=f"adapter_{i}")

    # Combine adapters with weights
    adapter_names = [f"adapter_{i}" for i in range(len(adapters))]
    weights = list(adapters.values())

    model.add_weighted_adapter(
        adapters=adapter_names,
        weights=weights,
        adapter_name="merged",
        combination_type="linear"
    )

    model.set_adapter("merged")
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(output_path)

    return merged_model

# Usage: Combine coding and chat adapters
# merge_multiple_adapters(
#     "meta-llama/Llama-3.1-8B",
#     {"./coding-lora": 0.6, "./chat-lora": 0.4},
#     "./merged-model"
# )
```

## Quantization

### GPTQ Quantization

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig
from datasets import load_dataset

def quantize_gptq(
    model_path: str,
    output_path: str,
    bits: int = 4,
    group_size: int = 128,
    calibration_samples: int = 128
):
    """
    Quantize model using GPTQ (post-training quantization).

    GPTQ provides excellent quality with 4-bit quantization.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Calibration dataset
    calibration_data = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    calibration_texts = calibration_data["text"][:calibration_samples]

    # Tokenize calibration data
    def tokenize(examples):
        return tokenizer(examples, truncation=True, max_length=2048)

    calibration_dataset = [tokenize(text) for text in calibration_texts if text.strip()]

    # GPTQ config
    gptq_config = GPTQConfig(
        bits=bits,
        group_size=group_size,
        dataset=calibration_dataset,
        desc_act=True,  # Activation order for better accuracy
        damp_percent=0.01,
        sym=True  # Symmetric quantization
    )

    # Load and quantize
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        quantization_config=gptq_config
    )

    # Save quantized model
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)

    print(f"Quantized model saved to {output_path}")
    return model

# Usage
# quantize_gptq("./merged-model", "./quantized-gptq-4bit")
```

### AWQ Quantization

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

def quantize_awq(
    model_path: str,
    output_path: str,
    bits: int = 4,
    group_size: int = 128,
    zero_point: bool = True
):
    """
    Quantize model using AWQ (Activation-aware Weight Quantization).

    AWQ is faster than GPTQ and often provides better quality.
    """
    # Load model with AWQ
    model = AutoAWQForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Quantization config
    quant_config = {
        "zero_point": zero_point,
        "q_group_size": group_size,
        "w_bit": bits,
        "version": "GEMM"  # GEMM for GPU, GEMV for CPU
    }

    # Quantize
    model.quantize(tokenizer, quant_config=quant_config)

    # Save
    model.save_quantized(output_path)
    tokenizer.save_pretrained(output_path)

    return model

# Usage
# quantize_awq("./merged-model", "./quantized-awq-4bit")
```

### GGUF Export (for llama.cpp)

```python
import subprocess
import os

def export_to_gguf(
    model_path: str,
    output_path: str,
    quantization: str = "q4_k_m"
):
    """
    Export model to GGUF format for llama.cpp inference.

    Quantization options:
    - q4_0, q4_1: Basic 4-bit
    - q4_k_s, q4_k_m: 4-bit with k-quants (recommended)
    - q5_0, q5_1, q5_k_s, q5_k_m: 5-bit variants
    - q8_0: 8-bit (highest quality)
    - f16: FP16 (no quantization)
    """
    llama_cpp_path = os.environ.get("LLAMA_CPP_PATH", "./llama.cpp")

    # Convert to GGUF
    convert_script = os.path.join(llama_cpp_path, "convert_hf_to_gguf.py")
    subprocess.run([
        "python", convert_script,
        model_path,
        "--outfile", f"{output_path}/model-f16.gguf",
        "--outtype", "f16"
    ], check=True)

    # Quantize
    quantize_binary = os.path.join(llama_cpp_path, "llama-quantize")
    subprocess.run([
        quantize_binary,
        f"{output_path}/model-f16.gguf",
        f"{output_path}/model-{quantization}.gguf",
        quantization
    ], check=True)

    # Clean up f16 file
    os.remove(f"{output_path}/model-f16.gguf")

    print(f"GGUF model saved: {output_path}/model-{quantization}.gguf")

# Usage
# export_to_gguf("./merged-model", "./gguf-output", "q4_k_m")
```

### Quantization Comparison

| Format | Size (8B model) | Speed | Quality | Use Case |
|--------|-----------------|-------|---------|----------|
| FP16 | ~16 GB | Baseline | 100% | Development, fine-tuning |
| GPTQ 4-bit | ~4 GB | ~1.5x | 98-99% | GPU inference |
| AWQ 4-bit | ~4 GB | ~1.8x | 98-99% | GPU inference (faster) |
| GGUF Q4_K_M | ~4.5 GB | ~2x | 97-98% | CPU + GPU, llama.cpp |
| GGUF Q5_K_M | ~5.5 GB | ~1.8x | 99% | Higher quality needs |

## Inference Optimization

### vLLM Deployment

```python
from vllm import LLM, SamplingParams

def deploy_with_vllm(
    model_path: str,
    tensor_parallel_size: int = 1,
    max_model_len: int = 4096,
    gpu_memory_utilization: float = 0.9
):
    """
    Deploy model with vLLM for high-throughput inference.

    vLLM provides:
    - Continuous batching
    - PagedAttention for efficient memory
    - Tensor parallelism for multi-GPU
    """
    llm = LLM(
        model=model_path,
        tensor_parallel_size=tensor_parallel_size,
        max_model_len=max_model_len,
        gpu_memory_utilization=gpu_memory_utilization,
        trust_remote_code=True,
        dtype="bfloat16"
    )

    return llm

def batch_inference_vllm(
    llm: LLM,
    prompts: list[str],
    max_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> list[str]:
    """Run batch inference with vLLM."""
    sampling_params = SamplingParams(
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p
    )

    outputs = llm.generate(prompts, sampling_params)

    return [output.outputs[0].text for output in outputs]

# Usage
# llm = deploy_with_vllm("./merged-model", tensor_parallel_size=2)
# responses = batch_inference_vllm(llm, ["Hello, how are you?", "What is AI?"])
```

### vLLM OpenAI-Compatible Server

```bash
# Start vLLM server with OpenAI-compatible API
python -m vllm.entrypoints.openai.api_server \
    --model ./merged-model \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 2 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.9
```

```python
# Client usage
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="./merged-model",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=256
)
print(response.choices[0].message.content)
```

### Text Generation Inference (TGI)

```yaml
# docker-compose.yml for TGI
version: "3.9"
services:
  tgi:
    image: ghcr.io/huggingface/text-generation-inference:latest
    ports:
      - "8080:80"
    volumes:
      - ./model:/data
    environment:
      - MODEL_ID=/data
      - NUM_SHARD=2
      - MAX_INPUT_LENGTH=2048
      - MAX_TOTAL_TOKENS=4096
      - QUANTIZE=bitsandbytes-nf4
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
```

```python
# TGI client usage
from huggingface_hub import InferenceClient

client = InferenceClient("http://localhost:8080")

response = client.text_generation(
    prompt="Hello, how are you?",
    max_new_tokens=256,
    temperature=0.7,
    do_sample=True
)
print(response)
```

## Production Deployment Patterns

### Model Server with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from contextlib import asynccontextmanager
import asyncio
from typing import Optional

class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    stop: Optional[list[str]] = None

class GenerationResponse(BaseModel):
    text: str
    tokens_generated: int
    finish_reason: str

# Global model reference
model = None
tokenizer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, tokenizer
    # Load model on startup
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        "./merged-model",
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("./merged-model")
    print("Model loaded!")
    yield
    # Cleanup on shutdown
    del model, tokenizer
    torch.cuda.empty_cache()

app = FastAPI(lifespan=lifespan)

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)

    # Run generation in thread pool to not block event loop
    loop = asyncio.get_event_loop()
    outputs = await loop.run_in_executor(
        None,
        lambda: model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            do_sample=request.temperature > 0,
            pad_token_id=tokenizer.pad_token_id
        )
    )

    generated_text = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )

    return GenerationResponse(
        text=generated_text,
        tokens_generated=len(outputs[0]) - inputs["input_ids"].shape[1],
        finish_reason="length" if len(outputs[0]) >= request.max_tokens else "stop"
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-inference
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llm-inference
  template:
    metadata:
      labels:
        app: llm-inference
    spec:
      containers:
        - name: llm
          image: your-registry/llm-server:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              nvidia.com/gpu: 1
              memory: "32Gi"
              cpu: "4"
            limits:
              nvidia.com/gpu: 1
              memory: "48Gi"
              cpu: "8"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 120
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 60
            periodSeconds: 10
          volumeMounts:
            - name: model-cache
              mountPath: /models
      volumes:
        - name: model-cache
          persistentVolumeClaim:
            claimName: model-pvc
      nodeSelector:
        nvidia.com/gpu.product: NVIDIA-A100-SXM4-80GB
---
apiVersion: v1
kind: Service
metadata:
  name: llm-inference
spec:
  selector:
    app: llm-inference
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

## Performance Benchmarking

```python
import time
import torch
from statistics import mean, stdev

def benchmark_inference(
    model,
    tokenizer,
    prompts: list[str],
    max_tokens: int = 256,
    warmup_runs: int = 3,
    benchmark_runs: int = 10
) -> dict:
    """
    Benchmark model inference performance.

    Returns latency, throughput, and memory metrics.
    """
    model.eval()

    # Warmup
    print("Warming up...")
    for _ in range(warmup_runs):
        inputs = tokenizer(prompts[0], return_tensors="pt").to(model.device)
        with torch.no_grad():
            model.generate(**inputs, max_new_tokens=max_tokens)

    # Clear cache
    torch.cuda.synchronize()
    torch.cuda.empty_cache()

    # Benchmark
    latencies = []
    tokens_generated = []

    print("Benchmarking...")
    for prompt in prompts[:benchmark_runs]:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        input_len = inputs["input_ids"].shape[1]

        torch.cuda.synchronize()
        start_time = time.perf_counter()

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=max_tokens)

        torch.cuda.synchronize()
        end_time = time.perf_counter()

        latency = end_time - start_time
        num_tokens = outputs.shape[1] - input_len

        latencies.append(latency)
        tokens_generated.append(num_tokens)

    # Memory stats
    memory_allocated = torch.cuda.max_memory_allocated() / 1024**3
    memory_reserved = torch.cuda.max_memory_reserved() / 1024**3

    avg_latency = mean(latencies)
    avg_tokens = mean(tokens_generated)

    return {
        "avg_latency_ms": avg_latency * 1000,
        "latency_std_ms": stdev(latencies) * 1000 if len(latencies) > 1 else 0,
        "avg_tokens_per_second": avg_tokens / avg_latency,
        "throughput_requests_per_second": 1 / avg_latency,
        "memory_allocated_gb": memory_allocated,
        "memory_reserved_gb": memory_reserved
    }

# Usage
# metrics = benchmark_inference(model, tokenizer, test_prompts)
# print(f"Latency: {metrics['avg_latency_ms']:.1f}ms")
# print(f"Throughput: {metrics['avg_tokens_per_second']:.1f} tokens/s")
```

## Quick Reference

### Deployment Decision Tree

```
Is latency critical (<100ms)?
├── Yes → Use vLLM with tensor parallelism
└── No
    ├── Is batch throughput priority?
    │   ├── Yes → Use vLLM or TGI
    │   └── No → Standard HF inference is fine
    └── Is memory constrained?
        ├── Yes → Use GGUF + llama.cpp or AWQ
        └── No → Use FP16 or GPTQ
```

### Quantization Selection

| Priority | Recommended Format |
|----------|-------------------|
| Maximum quality | FP16 (no quantization) |
| Best quality/size tradeoff | AWQ 4-bit or GGUF Q5_K_M |
| Minimum size | GGUF Q4_K_S or GPTQ 4-bit |
| CPU inference | GGUF Q4_K_M |
| Multi-GPU scaling | vLLM with FP16 or AWQ |

## Related References

- `lora-peft.md` - Adapter merging strategies
- `evaluation-metrics.md` - Post-deployment evaluation
- `hyperparameter-tuning.md` - Training configurations

---

## Reference: Evaluation Metrics

# Evaluation Metrics for Fine-Tuned Models

---

## Overview

Proper evaluation is critical for understanding fine-tuning success. This reference covers metrics, benchmarking strategies, and evaluation frameworks for fine-tuned language models.

## Core Metrics

### Perplexity

```python
import torch
import math
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.utils.data import DataLoader
from tqdm import tqdm

def calculate_perplexity(
    model,
    tokenizer,
    texts: list[str],
    batch_size: int = 8,
    max_length: int = 2048
) -> float:
    """
    Calculate perplexity on a test set.

    Lower perplexity = better language modeling performance.
    """
    model.eval()
    total_loss = 0
    total_tokens = 0

    encodings = tokenizer(
        texts,
        truncation=True,
        max_length=max_length,
        padding=True,
        return_tensors="pt"
    )

    dataset = torch.utils.data.TensorDataset(
        encodings["input_ids"],
        encodings["attention_mask"]
    )
    dataloader = DataLoader(dataset, batch_size=batch_size)

    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Calculating perplexity"):
            input_ids, attention_mask = batch
            input_ids = input_ids.to(model.device)
            attention_mask = attention_mask.to(model.device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=input_ids
            )

            # Count actual tokens (not padding)
            num_tokens = attention_mask.sum().item()
            total_loss += outputs.loss.item() * num_tokens
            total_tokens += num_tokens

    avg_loss = total_loss / total_tokens
    perplexity = math.exp(avg_loss)

    return perplexity

# Usage
# perplexity = calculate_perplexity(model, tokenizer, test_texts)
# print(f"Perplexity: {perplexity:.2f}")
```

### Generation-Based Metrics

```python
from evaluate import load
import numpy as np

def evaluate_generation(
    model,
    tokenizer,
    test_examples: list[dict],
    max_new_tokens: int = 256
) -> dict:
    """
    Evaluate model generation quality with multiple metrics.

    Args:
        test_examples: List of {"input": str, "reference": str}
    """
    # Load metrics
    bleu = load("bleu")
    rouge = load("rouge")
    bertscore = load("bertscore")

    predictions = []
    references = []

    model.eval()
    for example in tqdm(test_examples, desc="Generating"):
        inputs = tokenizer(example["input"], return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,  # Greedy for reproducibility
                pad_token_id=tokenizer.pad_token_id
            )

        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove input from prediction if model includes it
        prediction = prediction[len(example["input"]):].strip()

        predictions.append(prediction)
        references.append(example["reference"])

    # Calculate metrics
    results = {}

    # BLEU (0-100, higher is better)
    bleu_result = bleu.compute(predictions=predictions, references=[[r] for r in references])
    results["bleu"] = bleu_result["bleu"] * 100

    # ROUGE (0-1, higher is better)
    rouge_result = rouge.compute(predictions=predictions, references=references)
    results["rouge1"] = rouge_result["rouge1"]
    results["rouge2"] = rouge_result["rouge2"]
    results["rougeL"] = rouge_result["rougeL"]

    # BERTScore (0-1, higher is better)
    bertscore_result = bertscore.compute(
        predictions=predictions,
        references=references,
        lang="en"
    )
    results["bertscore_f1"] = np.mean(bertscore_result["f1"])

    return results

# Example
# metrics = evaluate_generation(model, tokenizer, test_data)
# print(f"BLEU: {metrics['bleu']:.2f}, ROUGE-L: {metrics['rougeL']:.4f}")
```

### Task-Specific Metrics

```python
from sklearn.metrics import accuracy_score, f1_score, classification_report
import re

def evaluate_classification(
    model,
    tokenizer,
    test_examples: list[dict],
    labels: list[str]
) -> dict:
    """
    Evaluate fine-tuned model on classification task.

    Args:
        test_examples: List of {"input": str, "label": str}
        labels: List of valid label strings
    """
    predictions = []
    true_labels = []

    model.eval()
    for example in tqdm(test_examples, desc="Classifying"):
        inputs = tokenizer(example["input"], return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=20,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id
            )

        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        prediction = prediction[len(example["input"]):].strip().lower()

        # Extract label from prediction
        predicted_label = None
        for label in labels:
            if label.lower() in prediction:
                predicted_label = label
                break

        if predicted_label is None:
            predicted_label = labels[0]  # Default to first label

        predictions.append(predicted_label)
        true_labels.append(example["label"])

    return {
        "accuracy": accuracy_score(true_labels, predictions),
        "f1_macro": f1_score(true_labels, predictions, average="macro"),
        "f1_weighted": f1_score(true_labels, predictions, average="weighted"),
        "classification_report": classification_report(true_labels, predictions)
    }

def evaluate_extraction(
    model,
    tokenizer,
    test_examples: list[dict]
) -> dict:
    """
    Evaluate information extraction tasks.

    Args:
        test_examples: List of {"input": str, "expected_entities": list[str]}
    """
    total_precision = 0
    total_recall = 0
    total_f1 = 0

    for example in test_examples:
        inputs = tokenizer(example["input"], return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, do_sample=False)

        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        prediction = prediction[len(example["input"]):].strip()

        # Extract entities (customize based on output format)
        predicted_entities = set(re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', prediction))
        expected_entities = set(example["expected_entities"])

        # Calculate metrics
        if len(predicted_entities) > 0:
            precision = len(predicted_entities & expected_entities) / len(predicted_entities)
        else:
            precision = 0

        if len(expected_entities) > 0:
            recall = len(predicted_entities & expected_entities) / len(expected_entities)
        else:
            recall = 1.0

        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0

        total_precision += precision
        total_recall += recall
        total_f1 += f1

    n = len(test_examples)
    return {
        "precision": total_precision / n,
        "recall": total_recall / n,
        "f1": total_f1 / n
    }
```

## Evaluation Framework

```python
from dataclasses import dataclass, field
from typing import Callable, Any
import json
from datetime import datetime

@dataclass
class EvaluationSuite:
    """Complete evaluation suite for fine-tuned models."""
    name: str
    metrics: dict[str, Callable] = field(default_factory=dict)
    results: dict[str, Any] = field(default_factory=dict)

    def add_metric(self, name: str, metric_fn: Callable):
        """Add a metric to the suite."""
        self.metrics[name] = metric_fn

    def run(self, model, tokenizer, test_data: dict) -> dict:
        """Run all metrics and return results."""
        self.results = {
            "model_name": getattr(model.config, "_name_or_path", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "metrics": {}
        }

        for metric_name, metric_fn in self.metrics.items():
            print(f"Running {metric_name}...")
            try:
                result = metric_fn(model, tokenizer, test_data.get(metric_name, test_data))
                self.results["metrics"][metric_name] = result
            except Exception as e:
                self.results["metrics"][metric_name] = {"error": str(e)}

        return self.results

    def save_results(self, path: str):
        """Save results to JSON file."""
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

    def compare_with(self, other_results: dict) -> dict:
        """Compare results with another evaluation."""
        comparison = {}
        for metric_name, value in self.results["metrics"].items():
            if metric_name in other_results.get("metrics", {}):
                other_value = other_results["metrics"][metric_name]
                if isinstance(value, (int, float)) and isinstance(other_value, (int, float)):
                    comparison[metric_name] = {
                        "current": value,
                        "baseline": other_value,
                        "delta": value - other_value,
                        "delta_pct": ((value - other_value) / other_value * 100)
                                     if other_value != 0 else 0
                    }
        return comparison

# Usage example
def create_evaluation_suite() -> EvaluationSuite:
    suite = EvaluationSuite(name="fine_tuning_eval")

    # Add perplexity
    suite.add_metric("perplexity", lambda m, t, d: calculate_perplexity(m, t, d["texts"]))

    # Add generation metrics
    suite.add_metric("generation", lambda m, t, d: evaluate_generation(m, t, d["generation"]))

    return suite

# Run evaluation
# suite = create_evaluation_suite()
# results = suite.run(model, tokenizer, test_data)
# suite.save_results("eval_results.json")
```

## Model Comparison

```python
import pandas as pd
from typing import Optional

class ModelComparison:
    """Compare multiple fine-tuned models."""

    def __init__(self):
        self.models = {}
        self.results = {}

    def add_model(self, name: str, model, tokenizer, adapter_path: Optional[str] = None):
        """Register a model for comparison."""
        self.models[name] = {
            "model": model,
            "tokenizer": tokenizer,
            "adapter_path": adapter_path
        }

    def evaluate_all(self, test_data: dict, metrics: list[str]) -> pd.DataFrame:
        """Evaluate all models and return comparison DataFrame."""
        all_results = []

        for model_name, model_info in self.models.items():
            model = model_info["model"]
            tokenizer = model_info["tokenizer"]

            model_results = {"model": model_name}

            for metric in metrics:
                if metric == "perplexity":
                    model_results["perplexity"] = calculate_perplexity(
                        model, tokenizer, test_data["texts"]
                    )
                elif metric == "generation":
                    gen_metrics = evaluate_generation(
                        model, tokenizer, test_data["generation"]
                    )
                    model_results.update(gen_metrics)

            all_results.append(model_results)
            self.results[model_name] = model_results

        return pd.DataFrame(all_results)

    def get_best_model(self, metric: str, higher_is_better: bool = True) -> str:
        """Return name of best performing model for a metric."""
        if not self.results:
            raise ValueError("No results available. Run evaluate_all first.")

        values = {name: r.get(metric, float('-inf') if higher_is_better else float('inf'))
                  for name, r in self.results.items()}

        if higher_is_better:
            return max(values, key=values.get)
        else:
            return min(values, key=values.get)

# Usage
# comparison = ModelComparison()
# comparison.add_model("base", base_model, tokenizer)
# comparison.add_model("lora_r8", lora_model_r8, tokenizer)
# comparison.add_model("lora_r16", lora_model_r16, tokenizer)
# df = comparison.evaluate_all(test_data, ["perplexity", "generation"])
# print(df)
```

## LLM-as-Judge Evaluation

```python
from openai import OpenAI
import json

def llm_judge_evaluation(
    predictions: list[str],
    references: list[str],
    inputs: list[str],
    judge_model: str = "gpt-4o",
    criteria: list[str] = None
) -> list[dict]:
    """
    Use LLM as judge to evaluate generation quality.

    Args:
        predictions: Model outputs
        references: Reference/gold outputs
        inputs: Original inputs
        judge_model: Model to use as judge
        criteria: Evaluation criteria (default: helpfulness, accuracy, coherence)
    """
    if criteria is None:
        criteria = ["helpfulness", "accuracy", "coherence", "relevance"]

    client = OpenAI()

    judge_prompt = """You are an expert evaluator. Rate the following model response on a scale of 1-5 for each criterion.

Input: {input}

Reference Response: {reference}

Model Response: {prediction}

Rate the model response on these criteria (1=poor, 5=excellent):
{criteria_list}

Return your ratings as JSON: {{"criterion_name": score, ...}}
Also include a brief explanation for each rating."""

    results = []

    for input_text, pred, ref in zip(inputs, predictions, references):
        prompt = judge_prompt.format(
            input=input_text,
            reference=ref,
            prediction=pred,
            criteria_list="\n".join(f"- {c}" for c in criteria)
        )

        response = client.chat.completions.create(
            model=judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # Parse response
        try:
            content = response.choices[0].message.content
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', content)
            if json_match:
                scores = json.loads(json_match.group())
            else:
                scores = {c: 3 for c in criteria}  # Default scores
        except:
            scores = {c: 3 for c in criteria}

        results.append({
            "input": input_text,
            "prediction": pred,
            "reference": ref,
            "scores": scores,
            "raw_response": content
        })

    # Aggregate scores
    aggregated = {c: [] for c in criteria}
    for r in results:
        for c in criteria:
            if c in r["scores"]:
                aggregated[c].append(r["scores"][c])

    summary = {c: sum(scores) / len(scores) if scores else 0
               for c, scores in aggregated.items()}

    return {
        "individual_results": results,
        "summary": summary
    }
```

## Benchmark Suites

```python
from lm_eval import evaluator
from lm_eval.models.huggingface import HFLM

def run_standard_benchmarks(
    model,
    tokenizer,
    tasks: list[str] = None,
    num_fewshot: int = 0
) -> dict:
    """
    Run standard LLM benchmarks using lm-evaluation-harness.

    Args:
        model: HuggingFace model
        tokenizer: Tokenizer
        tasks: List of tasks (default: common benchmarks)
        num_fewshot: Number of few-shot examples
    """
    if tasks is None:
        tasks = [
            "hellaswag",      # Commonsense reasoning
            "arc_easy",       # Science questions
            "arc_challenge",  # Harder science questions
            "winogrande",     # Commonsense reasoning
            "mmlu",           # Multi-task language understanding
            "truthfulqa_mc",  # Truthfulness
        ]

    # Wrap model for lm-eval
    lm = HFLM(pretrained=model, tokenizer=tokenizer)

    results = evaluator.simple_evaluate(
        model=lm,
        tasks=tasks,
        num_fewshot=num_fewshot,
        batch_size="auto"
    )

    # Extract key metrics
    summary = {}
    for task in tasks:
        if task in results["results"]:
            task_results = results["results"][task]
            # Get primary metric (usually accuracy)
            for key, value in task_results.items():
                if "acc" in key or "accuracy" in key:
                    summary[task] = value
                    break

    return {
        "full_results": results,
        "summary": summary
    }

# Usage with common benchmarks
BENCHMARK_TASKS = {
    "reasoning": ["hellaswag", "winogrande", "arc_easy", "arc_challenge"],
    "knowledge": ["mmlu", "triviaqa"],
    "code": ["humaneval", "mbpp"],
    "math": ["gsm8k", "math"],
    "safety": ["truthfulqa_mc", "toxigen"]
}
```

## Quick Reference

### Metric Selection by Task

| Task Type | Primary Metrics | Secondary Metrics |
|-----------|-----------------|-------------------|
| General Fine-Tuning | Perplexity, Loss | ROUGE, BLEU |
| Classification | Accuracy, F1 | Precision, Recall |
| Generation | ROUGE-L, BERTScore | Human eval, LLM-as-judge |
| Summarization | ROUGE-1/2/L | BERTScore, factuality |
| Translation | BLEU, chrF | TER, COMET |
| Code | pass@k, HumanEval | CodeBLEU |
| Chat/Assistant | LLM-as-judge | User preference |

### Interpreting Results

| Metric | Poor | Acceptable | Good | Excellent |
|--------|------|------------|------|-----------|
| Perplexity | >50 | 20-50 | 10-20 | <10 |
| BLEU | <20 | 20-40 | 40-60 | >60 |
| ROUGE-L | <0.3 | 0.3-0.5 | 0.5-0.7 | >0.7 |
| BERTScore F1 | <0.7 | 0.7-0.85 | 0.85-0.92 | >0.92 |
| Accuracy | <0.6 | 0.6-0.8 | 0.8-0.9 | >0.9 |

## Related References

- `hyperparameter-tuning.md` - Adjusting training based on eval results
- `dataset-preparation.md` - Creating evaluation sets
- `deployment-optimization.md` - Production evaluation considerations

---

## Reference: Hyperparameter Tuning

# Hyperparameter Tuning for LLM Fine-Tuning

---

## Overview

Hyperparameter selection significantly impacts fine-tuning success. This reference provides practical guidance for learning rates, batch sizes, schedulers, and optimization strategies tailored to LLM fine-tuning.

## Learning Rate Selection

### Guidelines by Fine-Tuning Method

| Method | Typical Range | Starting Point | Notes |
|--------|---------------|----------------|-------|
| Full Fine-Tuning | 1e-6 to 5e-5 | 2e-5 | Lower for larger models |
| LoRA | 1e-5 to 3e-4 | 2e-4 | Can use higher LR |
| QLoRA | 1e-5 to 2e-4 | 1e-4 | Similar to LoRA |
| Prefix Tuning | 1e-4 to 1e-2 | 3e-4 | Only training embeddings |

### Learning Rate Finder

```python
import torch
import matplotlib.pyplot as plt
from transformers import Trainer, TrainingArguments

def find_learning_rate(
    model,
    train_dataset,
    tokenizer,
    min_lr: float = 1e-7,
    max_lr: float = 1e-2,
    num_steps: int = 100
) -> tuple[list[float], list[float]]:
    """
    Find optimal learning rate using LR range test.

    Returns:
        Tuple of (learning_rates, losses)
    """
    # Create temporary training args with linearly increasing LR
    training_args = TrainingArguments(
        output_dir="./lr_finder",
        max_steps=num_steps,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=max_lr,
        warmup_steps=0,
        logging_steps=1,
        save_strategy="no",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer
    )

    # Custom LR schedule that increases exponentially
    lrs = []
    losses = []
    multiplier = (max_lr / min_lr) ** (1 / num_steps)

    current_lr = min_lr
    for step in range(num_steps):
        # Set LR
        for param_group in trainer.optimizer.param_groups:
            param_group['lr'] = current_lr

        # Training step
        loss = trainer.training_step(model, next(iter(trainer.get_train_dataloader())))

        lrs.append(current_lr)
        losses.append(loss.item())

        current_lr *= multiplier

        # Stop if loss explodes
        if loss.item() > losses[0] * 10:
            break

    return lrs, losses

def plot_lr_finder(lrs: list[float], losses: list[float]):
    """Plot learning rate finder results."""
    plt.figure(figsize=(10, 6))
    plt.semilogx(lrs, losses)
    plt.xlabel("Learning Rate")
    plt.ylabel("Loss")
    plt.title("Learning Rate Finder")

    # Find suggested LR (steepest descent)
    gradients = [(losses[i+1] - losses[i]) / (lrs[i+1] - lrs[i])
                 for i in range(len(losses) - 1)]
    suggested_idx = gradients.index(min(gradients))
    suggested_lr = lrs[suggested_idx]

    plt.axvline(x=suggested_lr, color='r', linestyle='--',
                label=f'Suggested LR: {suggested_lr:.2e}')
    plt.legend()
    plt.savefig("lr_finder.png")
    print(f"Suggested learning rate: {suggested_lr:.2e}")

    return suggested_lr
```

## Batch Size Optimization

### Effective Batch Size Calculation

```python
def calculate_training_config(
    target_batch_size: int,
    gpu_memory_gb: float,
    model_size_b: float,
    sequence_length: int = 2048,
    method: str = "qlora"
) -> dict:
    """
    Calculate optimal batch size and gradient accumulation.

    Args:
        target_batch_size: Desired effective batch size
        gpu_memory_gb: Available GPU memory
        model_size_b: Model size in billions
        sequence_length: Maximum sequence length
        method: "full", "lora", or "qlora"
    """
    # Memory estimation (rough heuristics)
    memory_per_param = {
        "full": 20,      # bf16 params + optimizer states + gradients
        "lora": 4,       # bf16 inference + small trainable
        "qlora": 1.5     # 4-bit + small trainable
    }

    base_memory_gb = model_size_b * memory_per_param[method]
    available_for_batch = gpu_memory_gb - base_memory_gb

    # Memory per sample (rough estimate)
    tokens_per_gb = 1000 * (8 / model_size_b)  # Rough scaling
    max_samples_in_memory = int(available_for_batch * tokens_per_gb / sequence_length)
    max_batch_per_device = max(1, max_samples_in_memory)

    # Calculate gradient accumulation
    gradient_accumulation = max(1, target_batch_size // max_batch_per_device)
    actual_batch_per_device = min(max_batch_per_device, target_batch_size // gradient_accumulation)

    effective_batch_size = actual_batch_per_device * gradient_accumulation

    return {
        "per_device_train_batch_size": actual_batch_per_device,
        "gradient_accumulation_steps": gradient_accumulation,
        "effective_batch_size": effective_batch_size,
        "estimated_memory_gb": base_memory_gb + (actual_batch_per_device * sequence_length / tokens_per_gb)
    }

# Example usage
config = calculate_training_config(
    target_batch_size=32,
    gpu_memory_gb=24,  # RTX 4090
    model_size_b=8,    # Llama 3.1 8B
    method="qlora"
)
print(config)
# {'per_device_train_batch_size': 4, 'gradient_accumulation_steps': 8, 'effective_batch_size': 32, ...}
```

### Batch Size Guidelines

| Dataset Size | Recommended Batch Size | Notes |
|--------------|------------------------|-------|
| < 1,000 | 8-16 | Small batch for more updates |
| 1,000 - 10,000 | 16-32 | Standard batch size |
| 10,000 - 100,000 | 32-64 | Larger batch for stability |
| > 100,000 | 64-128 | Can use larger batches |

## Learning Rate Schedulers

```python
from transformers import get_scheduler
import torch

def create_scheduler(
    optimizer,
    scheduler_type: str,
    num_training_steps: int,
    warmup_ratio: float = 0.03,
    min_lr_ratio: float = 0.1
):
    """
    Create learning rate scheduler.

    Args:
        scheduler_type: "cosine", "linear", "constant_with_warmup", "cosine_with_restarts"
        num_training_steps: Total training steps
        warmup_ratio: Fraction of steps for warmup
        min_lr_ratio: Minimum LR as fraction of max (for cosine)
    """
    num_warmup_steps = int(num_training_steps * warmup_ratio)

    if scheduler_type == "cosine":
        scheduler = get_scheduler(
            "cosine",
            optimizer=optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=num_training_steps
        )
    elif scheduler_type == "cosine_with_min_lr":
        # Custom cosine with minimum LR
        from torch.optim.lr_scheduler import CosineAnnealingLR, SequentialLR, LinearLR

        warmup = LinearLR(
            optimizer,
            start_factor=0.01,
            end_factor=1.0,
            total_iters=num_warmup_steps
        )
        cosine = CosineAnnealingLR(
            optimizer,
            T_max=num_training_steps - num_warmup_steps,
            eta_min=optimizer.defaults['lr'] * min_lr_ratio
        )
        scheduler = SequentialLR(
            optimizer,
            schedulers=[warmup, cosine],
            milestones=[num_warmup_steps]
        )
    elif scheduler_type == "constant_with_warmup":
        scheduler = get_scheduler(
            "constant_with_warmup",
            optimizer=optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=num_training_steps
        )
    else:
        scheduler = get_scheduler(
            scheduler_type,
            optimizer=optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=num_training_steps
        )

    return scheduler

# Scheduler comparison
SCHEDULER_GUIDE = """
Scheduler Selection:
- cosine: Best for most fine-tuning tasks, smooth decay
- linear: Good for short training runs
- constant_with_warmup: For very short fine-tuning or when LR is already optimal
- cosine_with_restarts: For longer training with periodic exploration
"""
```

### Visualizing Schedulers

```python
def visualize_schedulers(num_steps: int = 1000, warmup_ratio: float = 0.03):
    """Plot different scheduler behaviors."""
    import matplotlib.pyplot as plt

    schedulers_to_plot = ["cosine", "linear", "constant_with_warmup"]
    base_lr = 2e-4

    plt.figure(figsize=(12, 6))

    for sched_type in schedulers_to_plot:
        # Create dummy optimizer
        dummy_param = torch.nn.Parameter(torch.zeros(1))
        optimizer = torch.optim.AdamW([dummy_param], lr=base_lr)

        scheduler = create_scheduler(
            optimizer,
            scheduler_type=sched_type,
            num_training_steps=num_steps,
            warmup_ratio=warmup_ratio
        )

        lrs = []
        for _ in range(num_steps):
            lrs.append(optimizer.param_groups[0]['lr'])
            scheduler.step()

        plt.plot(lrs, label=sched_type)

    plt.xlabel("Step")
    plt.ylabel("Learning Rate")
    plt.title("Learning Rate Schedulers")
    plt.legend()
    plt.savefig("schedulers.png")
```

## Complete Training Configuration

```python
from transformers import TrainingArguments
from dataclasses import dataclass
from typing import Optional

@dataclass
class FineTuningConfig:
    """Complete fine-tuning configuration."""
    # Model
    model_name: str
    method: str = "qlora"  # "full", "lora", "qlora"

    # LoRA specific
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05

    # Training
    learning_rate: float = 2e-4
    num_epochs: int = 3
    batch_size: int = 32
    max_seq_length: int = 2048

    # Scheduler
    scheduler_type: str = "cosine"
    warmup_ratio: float = 0.03

    # Optimization
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_epsilon: float = 1e-8

    # Hardware
    gradient_checkpointing: bool = True
    bf16: bool = True
    tf32: bool = True

    # Evaluation
    eval_steps: int = 100
    save_steps: int = 100
    logging_steps: int = 10

def create_training_args(
    config: FineTuningConfig,
    output_dir: str,
    gpu_memory_gb: float
) -> TrainingArguments:
    """Create TrainingArguments from config."""

    # Calculate batch configuration
    batch_config = calculate_training_config(
        target_batch_size=config.batch_size,
        gpu_memory_gb=gpu_memory_gb,
        model_size_b=8,  # Estimate or pass as parameter
        sequence_length=config.max_seq_length,
        method=config.method
    )

    return TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=config.num_epochs,

        # Batch size
        per_device_train_batch_size=batch_config["per_device_train_batch_size"],
        per_device_eval_batch_size=batch_config["per_device_train_batch_size"],
        gradient_accumulation_steps=batch_config["gradient_accumulation_steps"],

        # Learning rate
        learning_rate=config.learning_rate,
        lr_scheduler_type=config.scheduler_type,
        warmup_ratio=config.warmup_ratio,

        # Optimization
        weight_decay=config.weight_decay,
        max_grad_norm=config.max_grad_norm,
        adam_beta1=config.adam_beta1,
        adam_beta2=config.adam_beta2,
        adam_epsilon=config.adam_epsilon,
        optim="paged_adamw_8bit" if config.method == "qlora" else "adamw_torch",

        # Hardware
        gradient_checkpointing=config.gradient_checkpointing,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        bf16=config.bf16,
        tf32=config.tf32,

        # Evaluation and saving
        eval_strategy="steps",
        eval_steps=config.eval_steps,
        save_strategy="steps",
        save_steps=config.save_steps,
        logging_steps=config.logging_steps,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,

        # Misc
        group_by_length=True,
        report_to=["wandb"],
        run_name=f"{config.model_name.split('/')[-1]}-{config.method}"
    )
```

## Hyperparameter Search

```python
from typing import Any
import optuna
from transformers import Trainer

def hyperparameter_search(
    model_init,
    train_dataset,
    eval_dataset,
    tokenizer,
    n_trials: int = 20,
    direction: str = "minimize"
) -> dict[str, Any]:
    """
    Run hyperparameter search using Optuna.

    Args:
        model_init: Function that returns initialized model
        n_trials: Number of trials to run
        direction: "minimize" for loss, "maximize" for accuracy
    """
    def hp_space(trial: optuna.Trial) -> dict:
        return {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 3e-4, log=True),
            "per_device_train_batch_size": trial.suggest_categorical(
                "per_device_train_batch_size", [2, 4, 8]
            ),
            "num_train_epochs": trial.suggest_int("num_train_epochs", 1, 5),
            "warmup_ratio": trial.suggest_float("warmup_ratio", 0.0, 0.1),
            "weight_decay": trial.suggest_float("weight_decay", 0.0, 0.1),
            "lr_scheduler_type": trial.suggest_categorical(
                "lr_scheduler_type", ["cosine", "linear", "constant_with_warmup"]
            )
        }

    training_args = TrainingArguments(
        output_dir="./hp_search",
        evaluation_strategy="epoch",
        save_strategy="no",
        report_to="none"
    )

    trainer = Trainer(
        model_init=model_init,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer
    )

    best_trial = trainer.hyperparameter_search(
        hp_space=hp_space,
        backend="optuna",
        n_trials=n_trials,
        direction=direction
    )

    return best_trial.hyperparameters

# Usage
# best_params = hyperparameter_search(model_init, train_ds, eval_ds, tokenizer)
```

## Monitoring Training

```python
from transformers import TrainerCallback
import wandb

class FineTuningCallback(TrainerCallback):
    """Custom callback for fine-tuning monitoring."""

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is None:
            return

        # Calculate additional metrics
        if "loss" in logs and state.global_step > 0:
            # Track loss velocity
            if hasattr(self, "prev_loss"):
                loss_delta = logs["loss"] - self.prev_loss
                logs["loss_delta"] = loss_delta
            self.prev_loss = logs["loss"]

    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        if metrics is None:
            return

        # Log evaluation metrics
        train_loss = state.log_history[-1].get("loss", 0) if state.log_history else 0
        eval_loss = metrics.get("eval_loss", 0)

        # Warn if overfitting
        if train_loss > 0 and eval_loss > train_loss * 1.5:
            print(f"Warning: Potential overfitting. Train loss: {train_loss:.4f}, Eval loss: {eval_loss:.4f}")

# Add to trainer
# trainer.add_callback(FineTuningCallback())
```

## Quick Reference

### Recommended Starting Configurations

**Small Dataset (<1K examples), QLoRA:**
```python
TrainingArguments(
    learning_rate=1e-4,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    weight_decay=0.05,
    max_grad_norm=0.3
)
```

**Medium Dataset (1K-10K examples), LoRA:**
```python
TrainingArguments(
    learning_rate=2e-4,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    weight_decay=0.01,
    max_grad_norm=1.0
)
```

**Large Dataset (>10K examples), Full Fine-Tuning:**
```python
TrainingArguments(
    learning_rate=2e-5,
    num_train_epochs=2,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    weight_decay=0.01,
    max_grad_norm=1.0
)
```

## Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Loss not decreasing | LR too low or too high | Use LR finder, try 10x or 0.1x |
| Loss spikes | LR too high, no warmup | Add warmup, reduce LR |
| Overfitting | Dataset too small, epochs too high | Reduce epochs, increase dropout |
| Underfitting | LR too low, rank too low (LoRA) | Increase LR, increase rank |
| OOM errors | Batch too large | Reduce batch, increase grad accum |

## Related References

- `lora-peft.md` - LoRA rank and alpha selection
- `evaluation-metrics.md` - Tracking training progress
- `dataset-preparation.md` - Dataset size impacts on hyperparameters

---

## Reference: Lora Peft

# LoRA and Parameter-Efficient Fine-Tuning

---

## Overview

Parameter-Efficient Fine-Tuning (PEFT) methods train only a small subset of model parameters while keeping the base model frozen. This dramatically reduces memory requirements and enables fine-tuning of large models on consumer hardware.

## When to Use PEFT vs Full Fine-Tuning

| Method | Use When | Avoid When |
|--------|----------|------------|
| **LoRA** | 7B+ models, limited VRAM, need multiple task adapters | Very small models (<1B), need maximum quality |
| **QLoRA** | 13B+ models, single GPU, memory-constrained | High-throughput training, inference speed critical |
| **Full Fine-Tuning** | Small models, abundant compute, maximum performance needed | Large models, limited resources |
| **Prefix Tuning** | Generation tasks, need interpretable soft prompts | Complex reasoning tasks |
| **IA3** | Extreme efficiency needed, inference overhead critical | Tasks needing high adapter capacity |

## LoRA Configuration

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="flash_attention_2"  # Use Flash Attention if available
)

# LoRA configuration for instruction tuning
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank - start with 8-16, increase if underfitting
    lora_alpha=32,                 # Alpha - typically 2x rank
    lora_dropout=0.05,             # Dropout for regularization
    target_modules=[               # Target attention layers
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj"       # MLP (optional, increases capacity)
    ],
    bias="none",                   # "none", "all", or "lora_only"
    modules_to_save=None           # Modules to train fully (e.g., embed_tokens for new tokens)
)

# Create PEFT model
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 13,631,488 || all params: 8,043,163,648 || trainable%: 0.1695
```

### Rank Selection Guide

```python
def recommend_lora_rank(task_complexity: str, dataset_size: int, model_size_b: float) -> int:
    """
    Recommend LoRA rank based on task and resources.

    Args:
        task_complexity: "simple" (classification), "moderate" (QA), "complex" (creative)
        dataset_size: Number of training examples
        model_size_b: Model size in billions of parameters
    """
    base_rank = {
        "simple": 8,
        "moderate": 16,
        "complex": 32
    }[task_complexity]

    # Adjust for dataset size
    if dataset_size < 1000:
        rank = max(4, base_rank // 2)  # Reduce rank to prevent overfitting
    elif dataset_size > 50000:
        rank = min(64, base_rank * 2)  # Can support higher rank
    else:
        rank = base_rank

    # Adjust for model size (larger models may need lower rank)
    if model_size_b > 30:
        rank = max(4, rank // 2)

    return rank

# Example usage
rank = recommend_lora_rank("moderate", dataset_size=10000, model_size_b=8)
print(f"Recommended rank: {rank}")  # 16
```

## QLoRA Configuration

QLoRA combines 4-bit quantization with LoRA for extreme memory efficiency.

```python
from transformers import BitsAndBytesConfig
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 for better quality
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True        # Nested quantization for more savings
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B",
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation="flash_attention_2"
)

# Prepare model for kbit training
from peft import prepare_model_for_kbit_training
model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

# Apply LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)
```

### Memory Comparison

| Model | Full FT | LoRA (r=16) | QLoRA (r=16) |
|-------|---------|-------------|--------------|
| Llama 3.1 8B | ~64 GB | ~18 GB | ~6 GB |
| Llama 3.1 70B | ~560 GB | ~160 GB | ~48 GB |
| Mistral 7B | ~56 GB | ~16 GB | ~5 GB |

## Training with PEFT

```python
from transformers import TrainingArguments, Trainer
from trl import SFTTrainer

training_args = TrainingArguments(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,      # Effective batch size = 16
    learning_rate=2e-4,                  # Higher LR for LoRA than full FT
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    evaluation_strategy="steps",
    eval_steps=100,
    bf16=True,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    optim="paged_adamw_8bit",            # Memory-efficient optimizer
    max_grad_norm=0.3,
    group_by_length=True,                # Group similar length sequences
    report_to="wandb"
)

# Using TRL's SFTTrainer for instruction tuning
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    max_seq_length=2048,
    packing=True,                        # Pack short sequences for efficiency
    dataset_text_field="text"
)

trainer.train()
```

## Target Module Selection

Different architectures have different module names:

```python
# Common target modules by architecture
TARGET_MODULES = {
    "llama": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    "mistral": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    "falcon": ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"],
    "gpt2": ["c_attn", "c_proj", "c_fc"],
    "phi": ["q_proj", "k_proj", "v_proj", "dense", "fc1", "fc2"],
    "qwen2": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
}

def get_target_modules(model_name: str, include_mlp: bool = True) -> list[str]:
    """Get appropriate target modules for a model architecture."""
    name_lower = model_name.lower()

    for arch, modules in TARGET_MODULES.items():
        if arch in name_lower:
            if include_mlp:
                return modules
            # Return only attention modules
            attention_keywords = ["q_proj", "k_proj", "v_proj", "o_proj", "query", "key", "value", "attn"]
            return [m for m in modules if any(kw in m.lower() for kw in attention_keywords)]

    # Default for unknown architectures - inspect model
    raise ValueError(f"Unknown architecture: {model_name}. Inspect model.named_modules() to find target modules.")
```

## Adapter Merging Strategies

```python
from peft import PeftModel

# Load base model and adapter
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
model = PeftModel.from_pretrained(base_model, "path/to/lora-adapter")

# Method 1: Merge adapter weights into base model
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")

# Method 2: Merge multiple adapters (weighted combination)
from peft import add_weighted_adapter

# Load multiple adapters
model = PeftModel.from_pretrained(base_model, "adapter1", adapter_name="adapter1")
model.load_adapter("adapter2", adapter_name="adapter2")
model.load_adapter("adapter3", adapter_name="adapter3")

# Combine with weights
model.add_weighted_adapter(
    adapters=["adapter1", "adapter2", "adapter3"],
    weights=[0.5, 0.3, 0.2],
    adapter_name="combined",
    combination_type="linear"  # or "svd", "cat"
)
model.set_adapter("combined")
```

## DoRA (Weight-Decomposed LoRA)

DoRA improves on LoRA by decomposing weights into magnitude and direction components.

```python
from peft import LoraConfig

# DoRA configuration
dora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    use_dora=True,  # Enable DoRA
    task_type=TaskType.CAUSAL_LM
)

# Training is identical to LoRA
model = get_peft_model(model, dora_config)
```

## rsLoRA (Rank-Stabilized LoRA)

Proper scaling for higher ranks:

```python
from peft import LoraConfig

# rsLoRA for high-rank training
rslora_config = LoraConfig(
    r=64,  # Higher rank
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    use_rslora=True,  # Rank-stabilized scaling
    task_type=TaskType.CAUSAL_LM
)
```

## Common Issues and Solutions

### Issue: Loss Not Decreasing

```python
# Check 1: Verify adapter is training
for name, param in model.named_parameters():
    if param.requires_grad:
        print(f"Training: {name}")

# Check 2: Increase rank or alpha
config = LoraConfig(r=32, lora_alpha=64, ...)

# Check 3: Reduce learning rate
training_args = TrainingArguments(learning_rate=1e-4, ...)
```

### Issue: Out of Memory

```python
# Solution 1: Use QLoRA
bnb_config = BitsAndBytesConfig(load_in_4bit=True, ...)

# Solution 2: Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Solution 3: Reduce batch size, increase gradient accumulation
training_args = TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16
)

# Solution 4: Use 8-bit optimizer
training_args = TrainingArguments(optim="paged_adamw_8bit")
```

### Issue: Adapter Not Loading

```python
# Ensure architecture matches
from peft import PeftModel, PeftConfig

# Check adapter config
config = PeftConfig.from_pretrained("path/to/adapter")
print(f"Base model: {config.base_model_name_or_path}")
print(f"Target modules: {config.target_modules}")

# Load with correct base model
base_model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)
model = PeftModel.from_pretrained(base_model, "path/to/adapter")
```

## Quick Reference

| Parameter | Typical Range | Effect |
|-----------|---------------|--------|
| `r` (rank) | 4-64 | Adapter capacity; higher = more expressive |
| `lora_alpha` | r to 2*r | Scaling factor; higher = larger updates |
| `lora_dropout` | 0.0-0.1 | Regularization; increase for small datasets |
| `learning_rate` | 1e-5 to 3e-4 | LoRA tolerates higher LR than full FT |
| `target_modules` | attention + MLP | More modules = more capacity + memory |

## Related References

- `hyperparameter-tuning.md` - Learning rate schedules, batch sizes
- `deployment-optimization.md` - Adapter merging, quantization for inference
- `dataset-preparation.md` - Training data formatting
