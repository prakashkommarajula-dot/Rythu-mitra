# Phase 6 Engineering Report: Smart Multilingual Agricultural Advisory System

**Project:** Rythu Mithra (రైతు మిత్ర) – AI-Based Multilingual Crop Disease and Pest Detection and Agricultural Advisory System  
**Phase:** 6 – Agricultural Advisory Engine, IPM Recommendations, Bilingual Dissemination, and Diagnostic Fallback  
**Date:** November 2026  
**Status:** Completed & Fully Verified (64/64 Unit and Integration Tests Passing)

---

## 1. Executive Summary

Phase 6 implements the intelligence and advisory layer of **Rythu Mithra**, bridging the machine learning prediction output (fine-tuned multilingual XLM-RoBERTa and computer vision models) to actionable, agronomically sound advisories for farmers. 

The advisory system is constructed strictly upon verified agricultural datasets (`cleaned_corpus.csv` and `diagnosis_fallback.csv`), adhering to guidelines set by ICAR (Indian Council of Agricultural Research), PJTSAU (Prof. Jayashankar Telangana State Agricultural University), and ANGRAU (Acharya N.G. Ranga Agricultural University).

Key achievements in Phase 6:
1. **Zero-Hallucination Verified Advice:** Chemical recommendations, active ingredients, organic remedies, and biological controls are retrieved solely from verified datasets. No synthetic pesticide dosages are fabricated.
2. **Comprehensive 9-Section IPM Dossier:** Structured Integrated Pest Management covering Pathogen Identification, Symptoms, Severity & Plant Parts, Diagnostic Questions, Cultural Control, Biological Control, Organic/Bio-pesticides, Chemical Control (with strict safety precautions & PPE), and Long-term Prevention.
3. **Diagnostic Fallback & Multi-Turn Follow-Up:** Farmers whose preliminary symptoms are vague or non-specific are guided with targeted field observation questions. An interactive multi-turn diagnostic API re-analyzes combined observations through the XLM-RoBERTa model without losing context.
4. **Complete Bilingual Parity:** Simultaneous Telugu (రైతు మిత్ర - సహజ / రసాయన యాజమాన్యం) and English display with Web Speech API audio narration.
5. **Auditing & Privacy Isolation:** Every advisory consultation is securely audited in the SQLite database (`advisory_views`), linking to the farmer's session while preventing cross-farmer data leakage.

---

## 2. Advisory Data Architecture

The advisory engine leverages two curated datasets processed during Phase 2:

### 2.1 Verified Cleaned Corpus (`data/processed/cleaned_corpus.csv`)
- **Total Records:** 1,386 verified observations across 14 major regional crops (Rice/Paddy, Cotton, Chilli, Bengal Gram, Maize, Red Gram, Tomato, Groundnut, Sugarcane, Soybean, Mango, Turmeric, Black Gram, Green Gram).
- **Disease & Pest Coverage:** 24 distinct pathogen classes mapped directly to Phase 3 classification targets.
- **Fields Indexed:**
  - `crop`, `disease_or_pest`, `symptoms`, `telugu_advisory`, `english_advisory`
  - Structured IPM controls: `cultural_control`, `biological_control`, `chemical_control`, `prevention`
  - Severity classification: `Mild`, `Moderate`, `Severe`
  - Scientific nomenclature: e.g., *Magnaporthe oryzae* (Blast), *Xanthomonas oryzae* (Bacterial Leaf Blight), *Helicoverpa armigera* (Pod Borer), *Spodoptera frugiperda* (Fall Armyworm).

### 2.2 Diagnostic Fallback Corpus (`data/processed/diagnosis_fallback.csv`)
- **Total Records:** 439 entries dedicated to `Requires further diagnosis`.
- **Purpose:** When farmer symptom descriptions are insufficient for confident classification (confidence threshold $p < 0.40$), this dataset supplies crop-specific diagnostic questionnaires (e.g., examining leaf collars, inspecting undersides of leaves with a hand lens, checking for waterlogged roots) and safe cultural interventions.

---

## 3. Core Components Implemented

### 3.1 Smart Advisory Engine (`services/advisory_service.py`)
- **`SmartAdvisoryEngine` Singleton:** Pre-loads datasets into memory on startup and indexes by `(disease_name, crop_name)` and `disease_name`.
- **Crop Alias Normalization (`normalize_crop_name`):** Normalizes Telugu, English, and regional dialect variations seamlessly:
  - Rice $\leftrightarrow$ Paddy (వరి)
  - Chickpea $\leftrightarrow$ Bengal Gram (శనగ)
  - Pigeonpea $\leftrightarrow$ Red Gram / Arhar / Tur (కంది)
  - Sorghum $\leftrightarrow$ Jowar (జొన్న)
  - Maize $\leftrightarrow$ Corn (మొక్కజొన్న)
- **`get_advisory(disease, crop, language)`:** Assembles the 9-point IPM advisory dictionary with biological controls, chemical options, and safety rules.
- **`get_fallback_advisory(crop, language)`:** Formulates diagnostic questions, warning notices, and safe cultural practices.
- **`log_advisory_view(...)`:** Records view logs into `advisory_views` table with user and prediction references.

### 3.2 Database Layer (`database/models.py` & `database/migrate_phase6.py`)
- Added `AdvisoryViewRecord` model:
  - `id`: Integer Primary Key
  - `user_id`: Foreign Key (`users.id`, nullable for guests)
  - `prediction_id`: Foreign Key (`nlp_predictions.id`, nullable)
  - `disease_or_pest`: String(100)
  - `crop`: String(100)
  - `language`: String(10)
  - `is_fallback`: Boolean
  - `viewed_at`: DateTime (UTC)
- Indexed on `user_id`, `prediction_id`, and `disease_or_pest` for fast retrieval and auditing.

### 3.3 Dynamic Routing & Multi-Turn Diagnostics (`routes/advisory_routes.py`)
- **`GET /advisory`:** Dual-mode rendering:
  - Direct/Deep-linked mode: Renders the full verified dossier or fallback diagnostic view based on query parameters (`disease`, `crop`, `prediction_id`, `needs_further_diagnosis`).
  - Catalog browsing mode: Displays a responsive grid of all 24 verified crop diseases and pests.
- **`POST /api/advisory/retrieve`:** JSON endpoint for asynchronous frontend retrieval.
- **`POST /api/predict/follow-up`:** Multi-turn diagnosis endpoint that concatenates initial ambiguous symptoms with new field observations and runs real-time inference with the fine-tuned XLM-RoBERTa model.
- **`GET /api/advisory/samples`:** Delivers sample bilingual queries for testing and demonstration.

### 3.4 User Interface Integration (`templates/advisory.html`, `templates/predict.html`, `static/js/app.js`)
- **Seamless Transition from Prediction to Advisory:** Upon NLP or Image prediction, a prominent button links directly to `/advisory?disease=...&crop=...&prediction_id=...` or opens the Diagnostic Fallback view if confidence is low.
- **Interactive Bilingual Toggle:** Farmers can switch between Telugu and English dynamically.
- **Integrated Voice Narration:** Web Speech API integration reads the advisory aloud in Telugu or English.
- **Safety Alert Banners:** Highlighting CIB&RC approved chemicals, mandatory PPE (gloves, masks, eye protection), pre-harvest intervals (PHI), and water source buffer distances.

---

## 4. Test Verification & Results

A dedicated test suite `tests/test_phase6_advisory.py` was developed alongside regression tests across all previous phases.

### Complete Test Results:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\PRAKASH\OneDrive\Desktop\Rythu_Mithra
collected 64 items

tests/test_dataset_preparation.py::test_processed_files_exist PASSED     [  1%]
tests/test_dataset_preparation.py::test_label_mapping_integrity PASSED   [  3%]
tests/test_dataset_preparation.py::test_zero_data_leakage_across_splits PASSED [  4%]
tests/test_dataset_preparation.py::test_all_classes_present_across_splits PASSED [  6%]
tests/test_dataset_preparation.py::test_telugu_unicode_preserved PASSED  [  7%]
tests/test_dataset_preparation.py::test_diagnosis_fallback_records PASSED [  9%]
tests/test_frontend.py::test_home_page_rendering PASSED                  [ 10%]
tests/test_frontend.py::test_login_and_register_pages_rendering PASSED   [ 12%]
tests/test_frontend.py::test_user_registration_and_login_flow PASSED     [ 14%]
tests/test_frontend.py::test_dashboard_rendering PASSED                  [ 15%]
tests/test_frontend.py::test_disease_prediction_page_and_form PASSED     [ 17%]
tests/test_frontend.py::test_image_detection_page_rendering PASSED       [ 18%]
tests/test_frontend.py::test_advisory_page_rendering PASSED              [ 20%]
tests/test_frontend.py::test_weather_alerts_page_rendering PASSED        [ 21%]
tests/test_frontend.py::test_history_page_rendering PASSED               [ 23%]
tests/test_frontend.py::test_about_page_rendering PASSED                 [ 25%]
tests/test_frontend.py::test_prediction_api_and_database_logging PASSED  [ 26%]
tests/test_nlp_predictor.py::test_model_loading_and_fallback_status PASSED [ 28%]
tests/test_nlp_predictor.py::test_correct_label_mapping PASSED           [ 29%]
tests/test_nlp_predictor.py::test_telugu_input PASSED                    [ 31%]
tests/test_nlp_predictor.py::test_english_input PASSED                   [ 32%]
tests/test_nlp_predictor.py::test_telugu_english_mixed_input PASSED      [ 34%]
tests/test_nlp_predictor.py::test_empty_input PASSED                     [ 35%]
tests/test_nlp_predictor.py::test_very_short_input PASSED                [ 37%]
tests/test_nlp_predictor.py::test_unknown_or_unclear_symptoms PASSED     [ 39%]
tests/test_nlp_predictor.py::test_prediction_api_success PASSED          [ 40%]
tests/test_nlp_predictor.py::test_prediction_api_missing_description PASSED [ 42%]
tests/test_phase5_auth.py::test_farmer_registration_success PASSED       [ 43%]
tests/test_phase5_auth.py::test_duplicate_mobile_registration_prevented PASSED [ 45%]
tests/test_phase5_auth.py::test_registration_validation_errors PASSED    [ 46%]
tests/test_phase5_auth.py::test_login_with_mobile_and_with_email PASSED  [ 48%]
tests/test_phase5_auth.py::test_invalid_login_handling PASSED            [ 50%]
tests/test_phase5_auth.py::test_logout_clears_session PASSED             [ 51%]
tests/test_phase5_auth.py::test_unauthorized_dashboard_and_history_access PASSED [ 53%]
tests/test_phase5_auth.py::test_nlp_prediction_linking_to_farmer PASSED  [ 54%]
tests/test_phase5_auth.py::test_farmer_to_farmer_data_isolation PASSED   [ 56%]
tests/test_phase5_auth.py::test_idor_protection_on_history_detail PASSED [ 57%]
tests/test_phase5_auth.py::test_history_filtering_search_and_crop PASSED [ 59%]
tests/test_phase5_auth.py::test_session_cookie_security_settings PASSED  [ 60%]
tests/test_phase5_auth.py::test_csrf_token_generation_and_validation PASSED [ 62%]
tests/test_phase6_advisory.py::test_advisory_retrieval_known_diseases PASSED [ 64%]
tests/test_phase6_advisory.py::test_advisory_retrieval_known_pests PASSED [ 65%]
tests/test_phase6_advisory.py::test_telugu_and_english_bilingual_advisory PASSED [ 67%]
tests/test_phase6_advisory.py::test_missing_or_unknown_advisory_handling PASSED [ 68%]
tests/test_phase6_advisory.py::test_crop_normalization_and_filtering PASSED [ 70%]
tests/test_phase6_advisory.py::test_fallback_diagnosis_workflow PASSED   [ 71%]
tests/test_phase6_advisory.py::test_chemical_safety_information PASSED   [ 73%]
tests/test_phase6_advisory.py::test_advisory_view_audit_logging PASSED   [ 75%]
tests/test_phase6_advisory.py::test_follow_up_prediction_api PASSED      [ 76%]
tests/test_phase6_advisory.py::test_advisory_page_rendering_modes PASSED [ 78%]
tests/test_routes.py::test_index_route PASSED                            [ 79%]
tests/test_routes.py::test_disease_detect_page PASSED                    [ 81%]
tests/test_routes.py::test_advisory_page PASSED                          [ 82%]
tests/test_routes.py::test_history_page PASSED                           [ 84%]
tests/test_routes.py::test_about_page PASSED                             [ 85%]
tests/test_routes.py::test_advisory_samples_api PASSED                   [ 87%]
tests/test_routes.py::test_advisory_query_api_telugu PASSED              [ 89%]
tests/test_routes.py::test_advisory_query_api_empty_query PASSED         [ 90%]
tests/test_disease_predict_missing_file PASSED                           [ 92%]
tests/test_services.py::test_allowed_file PASSED                         [ 93%]
tests/test_services.py::test_advisory_service_telugu PASSED              [ 95%]
tests/test_services.py::test_advisory_service_hindi PASSED               [ 96%]
tests/test_services.py::test_crop_disease_model_loader_missing_weights PASSED [ 98%]
tests/test_services.py::test_xlm_roberta_loader_missing_checkpoint PASSED [100%]

============================= 64 passed in 18.71s =============================
```

---

## 5. Summary of Deliverables

| Deliverable | File Path | Status |
|:---|:---|:---|
| Advisory Engine | `services/advisory_service.py` | Verified & Operational |
| Database Migration | `database/migrate_phase6.py` | Executed (Table `advisory_views` created) |
| Database Model | `database/models.py` (`AdvisoryViewRecord`) | Verified & Integrated |
| Route Handlers & Follow-up API | `routes/advisory_routes.py` | Verified & Operational |
| Prediction Integration | `routes/disease_routes.py` | Linked with advisory metadata |
| Modern Frontend Template | `templates/advisory.html` | Tested & Bilingual |
| Dynamic UI Client Logic | `static/js/app.js` | Tested & Interactive |
| Test Suite | `tests/test_phase6_advisory.py` | 10/10 Passed (Total 64/64 Passed) |
| Server Live Status | `http://localhost:5000` | Running & Accessible |
