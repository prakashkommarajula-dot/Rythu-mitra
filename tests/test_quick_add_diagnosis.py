"""
=============================================================================
Rythu Mithra - Targeted Quick Add & Diagnosis Test Suite
Tests:
1. Crop-specific Quick Add symptom chips API.
2. Verified dataset-derived symptoms for Groundnut, Rice, Cotton, Chilli, etc.
3. High-confidence crop disease predictions (Tikka Leaf Spot, Blast, Pink Bollworm).
4. Ambiguous symptoms triggering 'needs_further_diagnosis' and questions.
5. Interactive diagnosis refinement workflow with user answers.
6. Full 8-section actionable advisory payload validation.
7. Bilingual Telugu and English localization parity.
=============================================================================
"""

import pytest
from app import create_app
from database import db
from database.models import User, NLPPredictionRecord
from services.crop_symptoms_service import get_crop_symptoms, CROP_SYMPTOM_CATALOG
from services.nlp_predictor import predict_disease


@pytest.fixture
def app():
    """Create test application configured for testing."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# -----------------------------------------------------------------------------
# 1. Quick Add Crop Symptoms Catalog Tests
# -----------------------------------------------------------------------------

def test_crop_symptoms_service_groundnut():
    """Verify Groundnut returns Tikka Leaf Spot, Leaf Miner, Collar Rot chips."""
    res = get_crop_symptoms("Groundnut", lang="en")
    assert res["available"] is True
    assert res["crop"] == "Groundnut"
    assert len(res["symptoms"]) >= 5

    # Check for Tikka and Leaf Miner chips
    diseases = [s["disease"] for s in res["symptoms"]]
    assert "Tikka Leaf Spot" in diseases
    assert "Leaf Miner" in diseases

    # Verify bilingual labels exist
    for sym in res["symptoms"]:
        assert "label_en" in sym and len(sym["label_en"]) > 0
        assert "label_te" in sym and len(sym["label_te"]) > 0
        assert "symptom_en" in sym and len(sym["symptom_en"]) > 0
        assert "symptom_te" in sym and len(sym["symptom_te"]) > 0


def test_crop_symptoms_api_endpoint(client):
    """Test GET /api/crop-symptoms returns correct JSON payload."""
    response = client.get('/api/crop-symptoms?crop=Cotton&lang=en')
    assert response.status_code == 200
    data = response.get_json()
    assert data["available"] is True
    assert data["crop"] == "Cotton"
    assert len(data["symptoms"]) >= 4

    # Verify diagnostic questions are returned
    assert "diagnostic_questions" in data
    assert len(data["diagnostic_questions"]["en"]) > 0


def test_crop_symptoms_alias_normalization(client):
    """Verify alias normalization (Paddy -> Rice)."""
    response = client.get('/api/crop-symptoms?crop=Paddy&lang=te')
    assert response.status_code == 200
    data = response.get_json()
    assert data["available"] is True
    assert data["crop"] == "Rice"


# -----------------------------------------------------------------------------
# 2. Disease Prediction Tests
# -----------------------------------------------------------------------------

def test_groundnut_tikka_prediction():
    """Test clear Groundnut Tikka Leaf Spot description."""
    res = predict_disease(
        text="Dark brown circular spots with yellow halo appearing on leaves and premature shedding",
        crop="Groundnut",
        language="en"
    )
    assert res["success"] is True
    assert res["prediction"] == "Tikka Leaf Spot"
    assert res["needs_further_diagnosis"] is False
    assert res["score"] >= 0.85
    assert len(res["top_predictions"]) >= 3
    assert res["scientific_name"] != ""
    assert res["advisory"] is not None
    assert "chemical_control" in res["advisory"]


def test_rice_blast_prediction_telugu():
    """Test clear Rice Blast description in Telugu."""
    res = predict_disease(
        text="వరి ఆకులపై కండె ఆకారపు నూలు వంటి గోధుమ రంగు మచ్చలు ఏర్పడ్డాయి",
        crop="Rice",
        language="te"
    )
    assert res["success"] is True
    assert res["prediction"] == "Blast"
    assert res["needs_further_diagnosis"] is False
    assert res["score"] >= 0.85


def test_cotton_pink_bollworm_prediction():
    """Test clear Cotton Pink Bollworm description."""
    res = predict_disease(
        text="Rosetted flowers and bore holes on cotton bolls with stained lint",
        crop="Cotton",
        language="en"
    )
    assert res["success"] is True
    assert res["prediction"] == "Pink Bollworm"
    assert res["needs_further_diagnosis"] is False


def test_chilli_thrips_prediction():
    """Test clear Chilli Thrips description."""
    res = predict_disease(
        text="Leaves curling upward like boat shaped cups with silvery sheen on underside",
        crop="Chilli",
        language="en"
    )
    assert res["success"] is True
    assert res["prediction"] == "Thrips"
    assert res["needs_further_diagnosis"] is False


# -----------------------------------------------------------------------------
# 3. Ambiguous Symptoms & Interactive Refinement Workflow
# -----------------------------------------------------------------------------

def test_ambiguous_symptoms_trigger_further_diagnosis(client):
    """Test vague/generic symptom triggers needs_further_diagnosis and diagnostic questions."""
    response = client.post('/api/predict', json={
        "crop": "Groundnut",
        "crop_stage": "Vegetative",
        "description": "Leaves are yellowing and dry",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["prediction"] == "Requires further diagnosis"
    assert data["needs_further_diagnosis"] is True
    assert len(data["diagnostic_questions"]) > 0
    assert len(data["top_predictions"]) >= 3


def test_interactive_refinement_workflow(client):
    """Test refining an ambiguous diagnosis by submitting answers to diagnostic questions."""
    # First submit ambiguous
    res1 = client.post('/api/predict', json={
        "crop": "Groundnut",
        "description": "leaves turning yellow",
        "language": "en"
    })
    assert res1.get_json()["needs_further_diagnosis"] is True

    # Now refine with specific answers
    res2 = client.post('/api/predict', json={
        "crop": "Groundnut",
        "description": "leaves turning yellow",
        "answers": ["Dark brown circular spots with yellow halos are present on leaves"],
        "language": "en"
    })
    data2 = res2.get_json()
    assert data2["success"] is True
    assert data2["prediction"] == "Tikka Leaf Spot"
    assert data2["needs_further_diagnosis"] is False
    assert data2["score"] >= 0.85
    assert data2["advisory"] is not None
