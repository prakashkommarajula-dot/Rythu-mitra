#!/usr/bin/env python3
"""
=============================================================================
Rythu Mithra - AI-Based Multilingual Crop Disease & Pest Detection
Script: train_model.py
Phase 3: XLM-RoBERTa Model Training with Class-Weighted Cross-Entropy
=============================================================================
This script fine-tunes XLM-RoBERTa for multilingual crop disease and pest
classification across 23 target classes.

Key Requirements Followed:
1. Uses prepared training dataset (data/processed/train.csv).
2. Uses validation dataset (data/processed/val.csv) for model selection.
3. Does NOT use test data during training or model selection.
4. Uses class-weighted cross-entropy loss to address class imbalance.
5. Loads exact 23-class label mapping from data/processed/label_mapping.json.
6. Saves best model, tokenizer, and label mapping to models/crop_disease_xlmr_final/.
7. Records training and validation metrics.
=============================================================================
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_TRAIN_PATH = PROJECT_ROOT / "data" / "processed" / "train.csv"
DEFAULT_VAL_PATH = PROJECT_ROOT / "data" / "processed" / "val.csv"
DEFAULT_LABEL_MAPPING = PROJECT_ROOT / "data" / "processed" / "label_mapping.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "models" / "crop_disease_xlmr_final"


def parse_arguments():
    parser = argparse.ArgumentParser(description="Train XLM-RoBERTa for Rythu Mithra Crop Disease Detection")
    parser.add_argument("--train-path", type=str, default=str(DEFAULT_TRAIN_PATH), help="Path to train.csv")
    parser.add_argument("--val-path", type=str, default=str(DEFAULT_VAL_PATH), help="Path to val.csv")
    parser.add_argument("--label-mapping", type=str, default=str(DEFAULT_LABEL_MAPPING), help="Path to label_mapping.json")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR), help="Output directory for saved model")
    parser.add_argument("--model-name", type=str, default="xlm-roberta-base", help="Pretrained HuggingFace model backbone")
    parser.add_argument("--epochs", type=int, default=8, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size per device")
    parser.add_argument("--learning-rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--weight-decay", type=float, default=0.01, help="Weight decay")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--max-length", type=int, default=128, help="Max token sequence length")
    return parser.parse_args()


def load_dataset_csv(filepath):
    """Loads CSV and extracts texts and integer labels."""
    import csv
    texts = []
    labels = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get("model_input") or row.get("Farmer_Description", "")
            label = int(row["label_encoded"])
            texts.append(text)
            labels.append(label)
    return texts, labels


def compute_metrics_fn(eval_pred):
    """Computes accuracy, macro F1, and weighted F1."""
    import numpy as np
    from sklearn.metrics import accuracy_score, f1_score
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    macro_f1 = f1_score(labels, preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(labels, preds, average="weighted", zero_division=0)
    return {
        "accuracy": acc,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1
    }


def train():
    args = parse_arguments()

    print("=" * 65)
    print("🌾 Rythu Mithra - XLM-RoBERTa Disease & Pest Classifier Training")
    print("=" * 65)

    # 1. Check dependencies
    try:
        import torch
        from torch import nn
        import numpy as np
        from sklearn.utils.class_weight import compute_class_weight
        from transformers import (
            AutoTokenizer,
            AutoModelForSequenceClassification,
            TrainingArguments,
            Trainer,
            set_seed
        )
        from datasets import Dataset
    except ImportError as e:
        print(f"\n[!] Missing dependency for training: {e}")
        print("    Install required packages via:")
        print("    pip install torch transformers datasets scikit-learn pandas accelerate sentencepiece\n")
        sys.exit(1)

    set_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Execution device: {device}")
    if device.type == "cuda":
        print(f"[*] GPU Name: {torch.cuda.get_device_name(0)}")

    # 2. Load Label Mapping
    print(f"[*] Loading label mapping from: {args.label_mapping}")
    with open(args.label_mapping, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    num_classes = mapping_data["num_classes"]
    id2label = {int(k): v for k, v in mapping_data["id_to_label"].items()}
    label2id = mapping_data["label_to_id"]
    print(f"[+] Verified {num_classes} output classes.")

    # 3. Load Training & Validation Data
    print(f"[*] Loading training data from: {args.train_path}")
    train_texts, train_labels = load_dataset_csv(args.train_path)
    print(f"[+] Loaded {len(train_texts)} training samples.")

    print(f"[*] Loading validation data from: {args.val_path}")
    val_texts, val_labels = load_dataset_csv(args.val_path)
    print(f"[+] Loaded {len(val_texts)} validation samples.")

    # 4. Compute Class Weights for Balanced Cross-Entropy Loss
    print("[*] Computing balanced class weights...")
    unique_labels = np.unique(train_labels)
    class_weights_arr = compute_class_weight(
        class_weight="balanced",
        classes=unique_labels,
        y=train_labels
    )
    # Ensure tensor has entries for all num_classes
    full_weights = np.ones(num_classes, dtype=np.float32)
    for lbl, w in zip(unique_labels, class_weights_arr):
        full_weights[lbl] = w

    class_weights_tensor = torch.tensor(full_weights, dtype=torch.float32).to(device)
    print(f"[+] Class weights tensor computed (shape: {class_weights_tensor.shape}).")

    # 5. Initialize Tokenizer & Encode Datasets
    print(f"[*] Loading tokenizer for '{args.model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            padding="max_length",
            max_length=args.max_length
        )

    train_ds = Dataset.from_dict({"text": train_texts, "label": train_labels})
    val_ds = Dataset.from_dict({"text": val_texts, "label": val_labels})

    print("[*] Tokenizing datasets...")
    train_tokenized = train_ds.map(tokenize_function, batched=True)
    val_tokenized = val_ds.map(tokenize_function, batched=True)

    # 6. Initialize Model
    print(f"[*] Initializing AutoModelForSequenceClassification with num_labels={num_classes}...")
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=num_classes,
        id2label=id2label,
        label2id=label2id
    )
    model.to(device)

    # 7. Define Weighted Trainer
    class WeightedTrainer(Trainer):
        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            labels = inputs.get("labels")
            outputs = model(**inputs)
            logits = outputs.get("logits")
            loss_fct = nn.CrossEntropyLoss(weight=class_weights_tensor)
            loss = loss_fct(logits.view(-1, num_classes), labels.view(-1))
            return (loss, outputs) if return_outputs else loss

    # 8. Training Arguments
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(out_dir / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        logging_dir=str(out_dir / "logs"),
        logging_steps=10,
        save_total_limit=2,
        seed=args.seed,
        report_to="none"
    )

    trainer = WeightedTrainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=val_tokenized,
        compute_metrics=compute_metrics_fn
    )

    # 9. Execute Training
    print("\n[*] Starting XLM-RoBERTa model fine-tuning...")
    train_result = trainer.train()

    # 10. Evaluate on Validation Set
    print("\n[*] Evaluating best model on validation split...")
    val_metrics = trainer.evaluate(eval_dataset=val_tokenized)
    print(f"    - Validation Loss:     {val_metrics.get('eval_loss', 0):.4f}")
    print(f"    - Validation Accuracy: {val_metrics.get('eval_accuracy', 0):.4f}")
    print(f"    - Validation Macro F1: {val_metrics.get('eval_macro_f1', 0):.4f}")

    # 11. Save Model Artifacts
    print(f"\n[*] Saving final best model to: {out_dir}")
    trainer.save_model(str(out_dir))
    tokenizer.save_pretrained(str(out_dir))

    # Save verified label mapping alongside model
    with open(out_dir / "label_mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, ensure_ascii=False, indent=2)

    # Save training metrics history
    metrics_summary = {
        "model_name": args.model_name,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "train_samples": len(train_texts),
        "val_samples": len(val_texts),
        "validation_results": val_metrics,
        "train_runtime_seconds": train_result.metrics.get("train_runtime", 0)
    }
    with open(out_dir / "training_summary.json", "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, ensure_ascii=False, indent=2)

    print(f"[✓] Model, Tokenizer, and Metadata saved successfully to {out_dir}!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    train()
