# Rythu Mithra – Dataset Analysis & Preparation Report
**Phase 2: NLP Advisory & Disease Dataset Inspection**

---
## 1. Executive Summary
- **Total Raw Records:** 1620
- **Total Features / Columns:** 32
- **Full Exact Duplicate Rows Removed:** 234
- **Cleaned Retained Records:** 1386
- **Advisory Fallback Records (`Requires further diagnosis`):** 439
- **Confirmed Classification Records:** 882
- **Final Training Samples:** 328
- **Final Validation Samples:** 100
- **Final Testing Samples:** 113
- **Number of Disease/Pest Classes:** 23
- **Data Leakage Across Splits:** 0% (Verified Group-Stratified Partitioning)

---
## 2. Missing Values Analysis
| Column Name | Missing Count | Missing Percentage | Data Handling Decision |
|---|---|---|---|
| `Farmer_Description` | 20 | 1.23% | Dropped empty records (cannot train NLP on empty text) |
| `English_Translation` | 101 | 6.23% | Imputed with empty string / preserved in fallback |
| `Language` | 57 | 3.52% | Imputed with empty string / preserved in fallback |
| `State` | 14 | 0.86% | Imputed with empty string / preserved in fallback |
| `District` | 107 | 6.6% | Imputed with empty string / preserved in fallback |
| `Mandal` | 194 | 11.98% | Imputed with empty string / preserved in fallback |
| `Crop` | 8 | 0.49% | Imputed with empty string / preserved in fallback |
| `Crop_Local_Name` | 170 | 10.49% | Imputed with empty string / preserved in fallback |
| `Crop_Stage` | 141 | 8.7% | Imputed with empty string / preserved in fallback |
| `Season` | 131 | 8.09% | Imputed with empty string / preserved in fallback |
| `Month` | 134 | 8.27% | Imputed with empty string / preserved in fallback |
| `Symptoms` | 93 | 5.74% | Imputed with empty string / preserved in fallback |
| `Symptom_Keywords` | 171 | 10.56% | Imputed with empty string / preserved in fallback |
| `Disease_or_Pest` | 62 | 3.83% | Segregated invalid placeholders; verified 23 classes |
| `Problem_Type` | 583 | 35.99% | Imputed with empty string / preserved in fallback |
| `Scientific_Name` | 746 | 46.05% | Filled with empty string (optional field) |
| `Severity` | 118 | 7.28% | Imputed with empty string / preserved in fallback |
| `Confidence` | 117 | 7.22% | Imputed with empty string / preserved in fallback |
| `Diagnostic_Questions` | 1099 | 67.84% | Filled with empty string (optional field) |
| `Advisory_Telugu` | 41 | 2.53% | Imputed with empty string / preserved in fallback |
| `Advisory_English` | 81 | 5.0% | Imputed with empty string / preserved in fallback |
| `Organic_Management` | 773 | 47.72% | Filled with empty string (optional field) |
| `Biological_Control` | 847 | 52.28% | Filled with empty string (optional field) |
| `Cultural_Control` | 191 | 11.79% | Imputed with empty string / preserved in fallback |
| `Chemical_Control` | 91 | 5.62% | Imputed with empty string / preserved in fallback |
| `Prevention` | 186 | 11.48% | Imputed with empty string / preserved in fallback |
| `Safety_Precautions` | 111 | 6.85% | Imputed with empty string / preserved in fallback |
| `Source` | 102 | 6.3% | Imputed with empty string / preserved in fallback |
| `Verification_Status` | 147 | 9.07% | Imputed with empty string / preserved in fallback |
| `Intent` | 157 | 9.69% | Imputed with empty string / preserved in fallback |
| `Affected_Plant_Part` | 141 | 8.7% | Imputed with empty string / preserved in fallback |

---
## 3. Duplicate Records Analysis
- **Exact Full Row Duplicates:** 234 (Removed to prevent synthetic bias)
- **Total Farmer Descriptions:** 1620
- **Unique Farmer Descriptions:** 216
- **Duplicate Descriptions:** 1395
> **Key Insight:** Multiple records share templated descriptions across different districts or mandals. Standard random splitting causes massive data leakage where test descriptions appear in the training set. A **Stratified Group Split** based on `Farmer_Description` was strictly applied to ensure test descriptions are completely unseen during training.

---
## 4. Language Distribution & Telugu Unicode Preservation
| Language Category | Record Count | Percentage |
|---|---|---|
| Pure Telugu Unicode (`\u0C00` - `\u0C7F`) | 1529 | 94.38% |
| Mixed Telugu + English Code-Mixed | 71 | 4.38% |
| English ASCII Descriptions | 20 | 1.23% |

> **Unicode Preservation Rule:** All exports enforce UTF-8 without BOM (`utf-8`), preserving Telugu characters, vowel markers, and conjuncts accurately without mojibake.

---
## 5. Crop Distribution
| Crop Name | Count | Share (%) |
|---|---|---|
| Black Gram | 122 | 7.53% |
| Groundnut | 121 | 7.47% |
| Rice | 120 | 7.41% |
| Red Gram | 120 | 7.41% |
| Okra | 118 | 7.28% |
| Green Gram | 117 | 7.22% |
| Bengal Gram | 115 | 7.1% |
| Turmeric | 114 | 7.04% |
| Chilli | 114 | 7.04% |
| Maize | 112 | 6.91% |
| Cotton | 112 | 6.91% |
| Jowar | 111 | 6.85% |
| Brinjal | 109 | 6.73% |
| Tomato | 107 | 6.6% |

---
## 6. Disease & Pest Label Distribution & Class Imbalance
- **Majority Class:** `Pod Borer` (123 records)
- **Minority Class:** `Fruit and Shoot Borer` (32 records)
- **Imbalance Ratio:** 3.84:1
> **Crucial Rule Followed:** Rare disease classes (e.g., `Fruit and Shoot Borer`, `Shoot Fly`, `Leaf Miner` with ~29-32 samples) were **NOT deleted**. All 23 classes are fully represented in training, validation, and test splits.

| Class ID | Disease / Pest Label | Raw Count | Deduplicated Count |
|---|---|---|---|
| 0 | `Bacterial Wilt` | 36 | Preserved in splits |
| 1 | `Blast` | 40 | Preserved in splits |
| 2 | `Brown Planthopper` | 35 | Preserved in splits |
| 3 | `Early Blight` | 35 | Preserved in splits |
| 4 | `Fall Armyworm` | 35 | Preserved in splits |
| 5 | `Fruit Borer` | 68 | Preserved in splits |
| 6 | `Fruit and Shoot Borer` | 32 | Preserved in splits |
| 7 | `Fusarium Wilt` | 73 | Preserved in splits |
| 8 | `Grain Mold` | 38 | Preserved in splits |
| 9 | `Leaf Blotch` | 36 | Preserved in splits |
| 10 | `Leaf Curl Virus` | 35 | Preserved in splits |
| 11 | `Leaf Miner` | 38 | Preserved in splits |
| 12 | `Pink Bollworm` | 38 | Preserved in splits |
| 13 | `Pod Borer` | 123 | Preserved in splits |
| 14 | `Powdery Mildew` | 41 | Preserved in splits |
| 15 | `Rhizome Rot` | 35 | Preserved in splits |
| 16 | `Shoot Fly` | 34 | Preserved in splits |
| 17 | `Thrips` | 36 | Preserved in splits |
| 18 | `Tikka Leaf Spot` | 41 | Preserved in splits |
| 19 | `Turcicum Leaf Blight` | 36 | Preserved in splits |
| 20 | `Whitefly` | 78 | Preserved in splits |
| 21 | `Yellow Mosaic Virus` | 37 | Preserved in splits |
| 22 | `Yellow Vein Mosaic Virus` | 39 | Preserved in splits |

---
## 7. Preprocessing & Partitioning Decisions Summary
1. **Raw Preservation:** The original raw CSV is left completely unmodified.
2. **Advisory / Fallback Preservation:** All 439 `Requires further diagnosis` records are stored in `data/processed/diagnosis_fallback.csv` for the conversational advisory system.
3. **Composite Feature Construction:** Created `model_input` combining Farmer Description, Crop, Stage, Season, Symptoms, Keywords, and Affected Plant Part.
4. **Leakage-Free Partitioning:** Descriptions are grouped before stratified splitting. Overlap between train, validation, and test sets is **0%**.
5. **Label Encoding:** Integer encoding `0` to `22` is generated and saved to `data/processed/label_mapping.json`.