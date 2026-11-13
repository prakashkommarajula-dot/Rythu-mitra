"""
=============================================================================
Rythu Mithra - AI-Based Multilingual Crop Disease & Pest Detection
Test Suite: test_nlp_predictor.py
Phase 3: NLP Prediction Service & /api/predict Endpoint Verification
=============================================================================
Tests:
1. Telugu input
2. English input
3. Telugu-English code-mixed input
4. Empty input
5. Very short input
6. Unknown or unclear symptoms
7. Model loading status
8. Correct label mapping verification
9. Flask API endpoint POST /api/predict response
=============================================================================
"""

import sys
import json
try:
    import pytest
except ImportError:
    pytest = None
from pathlib import Path

# Ensure UTF-8 stdout on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from database import db
from services.nlp_predictor import get_predictor, predict_disease


@pytest.fixture
def client():
    """Configures a Flask test client using TestingConfig."""
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_model_loading_and_fallback_status():
    """Verify that predictor loads without crashing and reports status."""
    predictor = get_predictor()
    assert predictor is not None
    # Regardless of whether weights are placed or in fallback, id2label must be loaded
    assert len(predictor.id2label) == 23
    print(f"    [+] Predictor status: is_loaded={predictor.is_loaded}, device={predictor.device}")


def test_correct_label_mapping():
    """Verify that label mapping has 23 classes strictly matching label_mapping.json."""
    predictor = get_predictor()
    mapping_path = PROJECT_ROOT / "data" / "processed" / "label_mapping.json"
    with open(mapping_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data["classes"]) == 23
    assert len(predictor.id2label) == 23
    for idx, name in predictor.id2label.items():
        assert data["id_to_label"][str(idx)] == name


def test_telugu_input():
    """Test inference on genuine Telugu farmer query."""
    telugu_text = "వరి పంటలో ఆకులపై కండె ఆకారపు అగ్గి తెగులు మచ్చలు కనిపిస్తున్నాయి ఏం చేయాలి?"
    res = predict_disease(telugu_text, language="te")

    assert res["success"] is True
    assert "prediction" in res
    assert "score" in res
    assert isinstance(res["top_predictions"], list)
    assert "needs_further_diagnosis" in res
    assert "message" in res
    print(f"    [+] Telugu Prediction: '{res['prediction']}' (Score: {res['score']})")


def test_english_input():
    """Test inference on English farmer symptom description."""
    english_text = "Caterpillars boring into tomato and okra fruits with visible holes and frass."
    res = predict_disease(english_text, language="en")

    assert res["success"] is True
    assert "prediction" in res
    assert res["score"] > 0.0
    print(f"    [+] English Prediction: '{res['prediction']}' (Score: {res['score']})")


def test_telugu_english_mixed_input():
    """Test inference on Code-Mixed Telugu-English input."""
    mixed_text = "Chilli crop lo thrips మరియు తామర పురుగు ఆకులను ముడుచుకుపోయేలా చేస్తోంది."
    res = predict_disease(mixed_text, language="tel-en")

    assert res["success"] is True
    assert "prediction" in res
    print(f"    [+] Code-Mixed Prediction: '{res['prediction']}' (Score: {res['score']})")


def test_empty_input():
    """Test that empty or whitespace-only inputs trigger proper validation error."""
    res = predict_disease("")
    assert res["success"] is False
    assert res["needs_further_diagnosis"] is True
    assert "ఖాళీగా ఉంది" in res["message"] or "empty" in res["message"].lower()

    res_space = predict_disease("   ")
    assert res_space["success"] is False
    assert res_space["needs_further_diagnosis"] is True


def test_very_short_input():
    """Test that extremely short inputs (< 4 chars) trigger safe further diagnosis."""
    res = predict_disease("a")
    assert res["needs_further_diagnosis"] is True
    assert res["prediction"] == "Requires further diagnosis"
    assert "చిన్నదిగా" in res["message"] or "brief" in res["message"].lower()


def test_unknown_or_unclear_symptoms():
    """Test that ambiguous, non-specific inputs trigger needs_further_diagnosis."""
    vague_text = "నా పొలంలో ఏదో సమస్య ఉంది నాకు తెలియదు ఏమి చేయాలో"
    res = predict_disease(vague_text)

    assert "prediction" in res
    assert res["needs_further_diagnosis"] is True
    print(f"    [+] Unclear Symptoms Safety Check: needs_further_diagnosis={res['needs_further_diagnosis']}")


def test_prediction_api_success(client):
    """Test POST /api/predict endpoint returns expected schema."""
    payload = {
        "description": "టమాట కాయల మీద రంధ్రం చేసి పురుగు లోపలికి వెళ్ళినట్టు ఉంది ఏం చేయాలి?",
        "language": "te"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert "prediction" in data
    assert "score" in data
    assert "top_predictions" in data
    assert "needs_further_diagnosis" in data
    assert "message" in data
    print(f"    [+] API Endpoint Response: {data['prediction']} (Status 200)")


def test_prediction_api_missing_description(client):
    """Test POST /api/predict returns 400 when description is missing."""
    response = client.post("/api/predict", json={"language": "te"})
    assert response.status_code == 400

    data = response.get_json()
    assert data["success"] is False
    assert "Description field is required" in data["message"]


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌾 Running Rythu Mithra Phase 3 NLP Predictor Test Suite")
    print("=" * 60)

    test_model_loading_and_fallback_status()
    print("  [✓] Test 1: Model Loading & Fallback Status PASSED")

    test_correct_label_mapping()
    print("  [✓] Test 2: Label Mapping (23 classes) PASSED")

    test_telugu_input()
    print("  [✓] Test 3: Telugu Input Processing PASSED")

    test_english_input()
    print("  [✓] Test 4: English Input Processing PASSED")

    test_telugu_english_mixed_input()
    print("  [✓] Test 5: Code-Mixed Input Processing PASSED")

    test_empty_input()
    print("  [✓] Test 6: Empty Input Handling PASSED")

    test_very_short_input()
    print("  [✓] Test 7: Very Short Input Handling PASSED")

    test_unknown_or_unclear_symptoms()
    print("  [✓] Test 8: Unclear Symptoms Safe Further-Diagnosis PASSED")

    # API tests using test client
    app = create_app('testing')
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
        test_prediction_api_success(c)
        print("  [✓] Test 9: Flask POST /api/predict Success PASSED")

        test_prediction_api_missing_description(c)
        print("  [✓] Test 10: Flask POST /api/predict Validation 400 PASSED")

    print("\n" + "=" * 60)
    print("🎉 All 10 NLP Predictor Tests PASSED Successfully!")
    print("=" * 60 + "\n")
