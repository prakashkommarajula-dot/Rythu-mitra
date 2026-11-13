#!/usr/bin/env python3
"""
=============================================================================
Rythu Mithra - AI-Based Multilingual Crop Disease & Pest Detection
Script: evaluate_model.py
Phase 3: Untouched Test Set Evaluation & Language-Wise Benchmarking
=============================================================================
This script evaluates the fine-tuned XLM-RoBERTa model on the untouched test
dataset (data/processed/test.csv).

Generates:
1. Overall Accuracy, Macro F1, Weighted F1.
2. Per-class precision, recall, F1-score, and support.
3. Confusion matrix.
4. Language-wise evaluation (Telugu vs. English vs. Code-mixed).
5. Exports reports into reports/model_evaluation/.
=============================================================================
"""

import os
import sys
import csv
import json
import argparse
from pathlib import Path
from collections import defaultdict

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_DIR = PROJECT_ROOT / "models" / "crop_disease_xlmr_final"
DEFAULT_TEST_PATH = PROJECT_ROOT / "data" / "processed" / "test.csv"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "reports" / "model_evaluation"


def parse_arguments():
    parser = argparse.ArgumentParser(description="Evaluate XLM-RoBERTa on Rythu Mithra Test Set")
    parser.add_argument("--model-dir", type=str, default=str(DEFAULT_MODEL_DIR), help="Path to saved model directory")
    parser.add_argument("--test-path", type=str, default=str(DEFAULT_TEST_PATH), help="Path to test.csv")
    parser.add_argument("--report-dir", type=str, default=str(DEFAULT_REPORT_DIR), help="Output directory for reports")
    parser.add_argument("--batch-size", type=int, default=16, help="Evaluation batch size")
    return parser.parse_args()


def load_test_data(test_csv):
    """Loads test samples, labels, languages, and original texts."""
    rows = []
    with open(test_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def evaluate():
    args = parse_arguments()

    print("=" * 65)
    print("🌾 Rythu Mithra - XLM-RoBERTa Test Set Evaluation Pipeline")
    print("=" * 65)

    model_dir = Path(args.model_dir)
    test_file = Path(args.test_path)
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    # 1. Check if model exists
    if not model_dir.exists() or not (model_dir / "config.json").exists():
        print(f"[!] Saved model not found at: {model_dir}")
        print("    If model was trained in Colab, place the exported 'crop_disease_xlmr_final' folder in models/.")
        print("    Alternatively, execute 'python train_model.py' to train locally.\n")
        sys.exit(1)

    # 2. Check dependencies
    try:
        import torch
        import numpy as np
        from sklearn.metrics import (
            accuracy_score,
            f1_score,
            precision_score,
            recall_score,
            classification_report,
            confusion_matrix
        )
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
    except ImportError as e:
        print(f"[!] Missing dependency: {e}")
        print("    Install via: pip install torch transformers scikit-learn numpy\n")
        sys.exit(1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Execution device: {device}")

    # 3. Load Model and Tokenizer
    print(f"[*] Loading model and tokenizer from: {model_dir}")
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
    model.to(device)
    model.eval()

    # 4. Load Test Samples
    print(f"[*] Loading untouched test dataset from: {test_file}")
    test_rows = load_test_data(test_file)
    print(f"[+] Loaded {len(test_rows)} test samples.")

    # 5. Run Batched Inference
    test_texts = [r.get("model_input") or r.get("Farmer_Description", "") for r in test_rows]
    true_labels = [int(r["label_encoded"]) for r in test_rows]

    all_preds = []
    all_probs = []

    print("[*] Running inference on test split...")
    with torch.no_grad():
        for i in range(0, len(test_texts), args.batch_size):
            batch_texts = test_texts[i : i + args.batch_size]
            encoded = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=128,
                return_tensors="pt"
            ).to(device)
            outputs = model(**encoded)
            probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()
            preds = np.argmax(probs, axis=-1).tolist()
            all_preds.extend(preds)
            all_probs.extend(probs.tolist())

    # 6. Overall Metrics
    acc = accuracy_score(true_labels, all_preds)
    macro_f1 = f1_score(true_labels, all_preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(true_labels, all_preds, average="weighted", zero_division=0)

    print("\n" + "=" * 40)
    print("📊 Overall Test Set Evaluation Results:")
    print("=" * 40)
    print(f"   Accuracy:    {acc * 100:.2f}%")
    print(f"   Macro F1:    {macro_f1:.4f}")
    print(f"   Weighted F1: {weighted_f1:.4f}")

    # 7. Classification Report
    id2label = model.config.id2label
    target_names = [id2label[i] if i in id2label else str(i) for i in range(len(id2label))]

    clf_report = classification_report(
        true_labels,
        all_preds,
        target_names=target_names,
        digits=4,
        zero_division=0
    )
    print("\n--- Detailed Classification Report ---")
    print(clf_report)

    # 8. Confusion Matrix
    cm = confusion_matrix(true_labels, all_preds).tolist()

    # 9. Language-Wise Breakdown
    lang_breakdown = defaultdict(lambda: {"true": [], "pred": []})
    for r, t, p in zip(test_rows, true_labels, all_preds):
        desc = r.get("Farmer_Description", "")
        has_telugu = any("\u0C00" <= c <= "\u0C7F" for c in desc)
        has_english = any("a" <= c.lower() <= "z" for c in desc)
        if has_telugu and has_english:
            category = "Telugu-English Code-Mixed"
        elif has_telugu:
            category = "Pure Telugu"
        else:
            category = "English ASCII"

        lang_breakdown[category]["true"].append(t)
        lang_breakdown[category]["pred"].append(p)

    lang_results = {}
    print("\n--- Language-Wise Performance Breakdown ---")
    for category, d in lang_breakdown.items():
        sub_true = d["true"]
        sub_pred = d["pred"]
        sub_acc = accuracy_score(sub_true, sub_pred)
        sub_f1 = f1_score(sub_true, sub_pred, average="weighted", zero_division=0)
        lang_results[category] = {
            "samples": len(sub_true),
            "accuracy": round(sub_acc, 4),
            "weighted_f1": round(sub_f1, 4)
        }
        print(f"   {category:25} | Samples: {len(sub_true):3} | Acc: {sub_acc*100:6.2f}% | Weighted F1: {sub_f1:.4f}")

    # 10. Save Reports
    summary_metrics = {
        "model_path": str(model_dir),
        "test_dataset": str(test_file),
        "total_test_samples": len(test_rows),
        "accuracy": round(acc, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "language_evaluation": lang_results
    }

    with open(report_dir / "test_metrics.json", "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, ensure_ascii=False, indent=2)

    with open(report_dir / "classification_report.txt", "w", encoding="utf-8") as f:
        f.write(clf_report)

    with open(report_dir / "confusion_matrix.json", "w", encoding="utf-8") as f:
        json.dump({"labels": target_names, "matrix": cm}, f, ensure_ascii=False, indent=2)

    with open(report_dir / "language_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(lang_results, f, ensure_ascii=False, indent=2)

    print(f"\n[✓] Reports saved successfully to: {report_dir}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    evaluate()
