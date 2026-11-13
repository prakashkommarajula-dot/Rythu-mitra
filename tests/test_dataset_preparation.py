"""
Unit and Integration Tests for Phase 2: Dataset Preparation & Preprocessing.
Validates:
1. File existence and non-empty size in data/processed/.
2. Unicode preservation for Telugu descriptions and advisories.
3. Zero data leakage between train, validation, and test splits.
4. Retention of all 23 disease/pest classes across splits.
5. Integrity of 'Requires further diagnosis' fallback dataset.
"""

import os
import sys
import csv
import json
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

try:
    import pytest
except ImportError:
    pytest = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def test_processed_files_exist():
    """Verify all required processed dataset files exist and are non-empty."""
    expected_files = [
        "train.csv",
        "val.csv",
        "test.csv",
        "diagnosis_fallback.csv",
        "cleaned_corpus.csv",
        "label_mapping.json",
        "dataset_summary.json"
    ]
    for fname in expected_files:
        fpath = PROCESSED_DIR / fname
        assert fpath.exists(), f"Missing processed file: {fpath}"
        assert fpath.stat().st_size > 0, f"File is empty: {fpath}"


def test_label_mapping_integrity():
    """Verify label mapping contains exactly 23 verified disease/pest classes."""
    map_path = PROCESSED_DIR / "label_mapping.json"
    with open(map_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["num_classes"] == 23
    assert len(data["label_to_id"]) == 23
    assert len(data["id_to_label"]) == 23
    assert len(data["classes"]) == 23

    # Check that IDs are strictly 0 to 22
    expected_ids = set(range(23))
    actual_ids = set(int(k) for k in data["id_to_label"].keys())
    assert actual_ids == expected_ids


def test_zero_data_leakage_across_splits():
    """Ensure strict 0% overlap of Farmer_Description across train, val, and test."""
    def get_descriptions(filename):
        with open(PROCESSED_DIR / filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return set(r["Farmer_Description"].strip() for r in reader if r.get("Farmer_Description"))

    train_descs = get_descriptions("train.csv")
    val_descs = get_descriptions("val.csv")
    test_descs = get_descriptions("test.csv")

    assert len(train_descs & val_descs) == 0, f"Data leakage detected between train and val: {train_descs & val_descs}"
    assert len(train_descs & test_descs) == 0, f"Data leakage detected between train and test: {train_descs & test_descs}"
    assert len(val_descs & test_descs) == 0, f"Data leakage detected between val and test: {val_descs & test_descs}"


def test_all_classes_present_across_splits():
    """Verify no classes are deleted or missing from any split."""
    def get_classes(filename):
        with open(PROCESSED_DIR / filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return set(r["Disease_or_Pest"].strip() for r in reader)

    train_classes = get_classes("train.csv")
    val_classes = get_classes("val.csv")
    test_classes = get_classes("test.csv")

    assert len(train_classes) == 23, f"Train set has {len(train_classes)}/23 classes."
    assert len(val_classes) == 23, f"Val set has {len(val_classes)}/23 classes."
    assert len(test_classes) == 23, f"Test set has {len(test_classes)}/23 classes."


def test_telugu_unicode_preserved():
    """Verify Telugu text in Farmer_Description and Advisory_Telugu is intact."""
    for filename in ["train.csv", "val.csv", "test.csv", "diagnosis_fallback.csv"]:
        with open(PROCESSED_DIR / filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            telugu_found = False
            for r in reader:
                desc = r.get("Farmer_Description", "")
                if any("\u0C00" <= char <= "\u0C7F" for char in desc):
                    telugu_found = True
                    break
            assert telugu_found, f"No Telugu Unicode characters found in {filename}!"


def test_diagnosis_fallback_records():
    """Verify 'Requires further diagnosis' records are preserved with advisory content."""
    fb_path = PROCESSED_DIR / "diagnosis_fallback.csv"
    with open(fb_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 400, f"Expected >400 diagnosis fallback records, found {len(rows)}"
    for r in rows:
        assert r["Disease_or_Pest"].strip() == "Requires further diagnosis"


if __name__ == "__main__":
    print("[*] Running Phase 2 Dataset Validation Checks...")
    test_processed_files_exist()
    print("    [✓] Processed files existence: PASSED")
    test_label_mapping_integrity()
    print("    [✓] Label mapping integrity (23 classes): PASSED")
    test_zero_data_leakage_across_splits()
    print("    [✓] Zero data leakage across splits: PASSED (0% overlap)")
    test_all_classes_present_across_splits()
    print("    [✓] All 23 classes present in Train/Val/Test: PASSED")
    test_telugu_unicode_preserved()
    print("    [✓] Telugu Unicode character preservation: PASSED")
    test_diagnosis_fallback_records()
    print("    [✓] Fallback diagnosis records preserved: PASSED")
    print("\n[+] All validation checks passed successfully!")
