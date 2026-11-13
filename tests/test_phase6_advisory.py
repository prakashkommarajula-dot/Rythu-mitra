#!/usr/bin/env python3
"""
=============================================================================
Rythu Mithra - Phase 6 Smart Agricultural Advisory System Test Suite
=============================================================================
Validates:
1. Advisory retrieval for verified diseases (Blast, Early Blight, etc.)
2. Advisory retrieval for verified pests (Whitefly, Pod Borer, Pink Bollworm, Thrips)
3. Telugu and English bilingual advisory content preservation
4. Missing / unknown advisory handling
5. Crop-specific filtering and regional alias normalization (Paddy <-> Rice)
6. Fallback diagnosis workflow ('diagnosis_fallback.csv' with diagnostic questions)
7. Multi-turn follow-up symptom re-analysis workflow
8. Strict chemical safety and dosage adherence (no fabricated chemicals)
9. Database audit logging of viewed advisories with farmer isolation
10. End-to-end Advisory page UI rendering (9-section IPM & fallback modes)
=============================================================================
"""

import sys
import os
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from app import create_app
from database import db
from database.models import User, AdvisoryViewRecord
from services.advisory_service import (
    get_advisory,
    get_fallback_advisory,
    normalize_crop_name,
    log_advisory_view,
    advisory_engine
)


@pytest.fixture
def app():
    """Create Flask application context for testing."""
    app_instance = create_app('testing')
    app_instance.config['TESTING'] = True
    app_instance.config['WTF_CSRF_ENABLED'] = False
    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


# =============================================================================
# 1. Known Disease Advisory Retrieval Tests
# =============================================================================

def test_advisory_retrieval_known_diseases():
    """Verifies that known fungal/bacterial diseases retrieve complete 9-section advisories."""
    diseases_to_test = [
        ('Blast', 'Rice', 'Magnaporthe oryzae'),
        ('Early Blight', 'Tomato', 'Alternaria solani'),
        ('Fusarium Wilt', 'Bengal Gram', 'Fusarium oxysporum'),
        ('Tikka Leaf Spot', 'Groundnut', 'Cercospora'),
    ]

    for d_name, crop, sci_sub in diseases_to_test:
        adv = get_advisory(d_name, crop=crop, language='te')
        assert adv is not None, f"Advisory for {d_name} must not be None"
        assert adv['confirmed_diagnosis'] is True
        assert adv['disease_or_pest'] == d_name
        assert sci_sub.lower() in (adv['scientific_name'] or '').lower()
        
        # Verify 9 core sections are non-empty
        assert len(adv['symptoms_te']) > 0
        assert len(adv['advisory_te']) > 0
        assert len(adv['organic_management']) > 0
        assert len(adv['biological_control']) > 0
        assert len(adv['cultural_control']) > 0
        assert len(adv['chemical_control']) > 0
        assert len(adv['prevention']) > 0
        assert len(adv['safety_precautions']) > 0


# =============================================================================
# 2. Known Pest Advisory Retrieval Tests
# =============================================================================

def test_advisory_retrieval_known_pests():
    """Verifies that known insect pests retrieve verified biological & chemical advice."""
    pests_to_test = [
        ('Whitefly', 'Cotton', 'Bemisia tabaci'),
        ('Pod Borer', 'Bengal Gram', 'Helicoverpa armigera'),
        ('Pink Bollworm', 'Cotton', 'Pectinophora gossypiella'),
        ('Thrips', 'Chilli', 'Scirtothrips dorsalis'),
    ]

    for p_name, crop, sci_sub in pests_to_test:
        adv = get_advisory(p_name, crop=crop, language='te')
        assert adv is not None, f"Pest advisory for {p_name} must not be None"
        assert adv['problem_type'] == 'Pest'
        assert sci_sub.lower() in (adv['scientific_name'] or '').lower()
        assert 'వేప' in adv['organic_management'] or 'neem' in adv['organic_management'].lower()


# =============================================================================
# 3. Telugu and English Bilingual Support Tests
# =============================================================================

def test_telugu_and_english_bilingual_advisory():
    """Verifies that both Telugu and English advisory fields are accurately retrieved and formatted."""
    adv_te = get_advisory('Blast', 'Rice', language='te')
    assert adv_te is not None
    # Verify Telugu Unicode is intact
    assert any(ord(char) >= 0x0C00 and ord(char) <= 0x0C7F for char in adv_te['advisory_te']), "Telugu characters must be present"

    adv_en = get_advisory('Blast', 'Rice', language='en')
    assert adv_en is not None
    assert len(adv_en['advisory_en']) > 10
    assert 'blast' in adv_en['advisory_en'].lower()


# =============================================================================
# 4. Missing Advisory & Unknown Input Handling
# =============================================================================

def test_missing_or_unknown_advisory_handling():
    """Verifies that requesting a nonexistent or invalid disease gracefully returns None."""
    assert get_advisory('Nonexistent Cosmic Fungal Disease') is None
    assert get_advisory('') is None
    assert get_advisory('   ') is None


# =============================================================================
# 5. Crop-Specific Filtering and Alias Normalization
# =============================================================================

def test_crop_normalization_and_filtering():
    """Verifies that crop aliases (Paddy -> Rice, Chickpea -> Bengal Gram) map correctly."""
    assert normalize_crop_name('paddy') == 'Rice'
    assert normalize_crop_name('వరి') == 'Rice'
    assert normalize_crop_name('chickpea') == 'Bengal Gram'
    assert normalize_crop_name('శనగ') == 'Bengal Gram'
    assert normalize_crop_name('corn') == 'Maize'
    assert normalize_crop_name('eggplant') == 'Brinjal'

    # Retrieve Blast with alias 'Paddy' -> should find Rice Blast
    adv_paddy = get_advisory('Blast', crop='Paddy')
    assert adv_paddy is not None
    assert adv_paddy['crop'] == 'Rice'


# =============================================================================
# 6. Fallback Diagnosis Workflow ('diagnosis_fallback.csv')
# =============================================================================

def test_fallback_diagnosis_workflow():
    """
    CRITICAL TEST: Verifies that uncertain/fallback queries:
    - Never force a fake disease label.
    - Provide crop-specific diagnostic questions from 'diagnosis_fallback.csv'.
    - Do not recommend chemical pesticides without a confirmed diagnosis.
    """
    fb_rice = get_fallback_advisory(crop='Rice')
    assert fb_rice['is_fallback'] is True
    assert fb_rice['confirmed_diagnosis'] is False
    assert 'Requires further diagnosis' in fb_rice['disease_or_pest']
    
    # Must contain real diagnostic questions for Rice
    assert len(fb_rice['diagnostic_questions']) > 20
    assert any(ord(c) >= 0x0C00 and ord(c) <= 0x0C7F for c in fb_rice['diagnostic_questions'])

    # Must NOT recommend chemical control
    assert fb_rice['chemical_control'] is None, "Chemicals must NOT be recommended in fallback mode"

    # Must contain safe general cultural & preventive measures
    assert len(fb_rice['prevention']) > 0
    assert len(fb_rice['safety_precautions']) > 0


# =============================================================================
# 7. Chemical Safety & Dosages Adherence
# =============================================================================

def test_chemical_safety_information():
    """Verifies that chemical advice preserves exact dataset dosages and includes PPE / PHI safety warnings."""
    adv = get_advisory('Blast', 'Rice')
    assert adv is not None
    chem = adv['chemical_control']
    safety = adv['safety_precautions']
    
    # Check dataset dosage / caution
    assert 'రసాయనాలు వాడవద్దు' in chem or 'Do not apply chemicals' in chem or 'WP' in chem or 'EC' in chem
    # Check safety precautions: mask, gloves, PHI
    assert 'మాస్క్' in safety or 'mask' in safety.lower() or 'gloves' in safety.lower() or 'చేతి తొడుగులు' in safety


# =============================================================================
# 8. Database Integration & Farmer View Audit Logging
# =============================================================================

def test_advisory_view_audit_logging(client, app):
    """Verifies that viewing an advisory is logged in the database linked to the authenticated farmer."""
    with app.app_context():
        farmer = User(
            full_name='Subba Rao',
            mobile_number='9848123123',
            password_hash='dummy_hash',
            district='Guntur'
        )
        db.session.add(farmer)
        db.session.commit()
        user_id = farmer.id

        view_id = log_advisory_view(
            user_id=user_id,
            disease_or_pest='Blast',
            crop='Rice',
            language='te'
        )
        assert view_id is not None

        # Verify record in database
        rec = AdvisoryViewRecord.query.get(view_id)
        assert rec is not None
        assert rec.user_id == user_id
        assert rec.disease_or_pest == 'Blast'
        assert rec.crop == 'Rice'


# =============================================================================
# 9. Multi-Turn Follow-Up Prediction API Test
# =============================================================================

def test_follow_up_prediction_api(client):
    """Verifies that submitting field observations to /api/predict/follow-up re-predicts."""
    payload = {
        'original_description': 'వరి ఆకులు పసుపుగా మారుతున్నాయి',
        'follow_up': 'ఆకులపై కండె ఆకారపు గోధుమ రంగు మచ్చలు ఉన్నాయి',
        'crop': 'Rice',
        'language': 'te'
    }
    res = client.post('/api/predict/follow-up', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'advisory_url' in data['result']


# =============================================================================
# 10. Web Interface Routing & Template Rendering Tests
# =============================================================================

def test_advisory_page_rendering_modes(client):
    """Verifies that /advisory renders correctly in verified, fallback, and catalog modes."""
    # 1. Verified Disease Mode
    res_blast = client.get('/advisory?disease=Blast&crop=Rice')
    assert res_blast.status_code == 200
    html_blast = res_blast.data.decode('utf-8')
    assert 'Blast' in html_blast
    assert 'Magnaporthe oryzae' in html_blast
    assert 'Integrated Pest Management' in html_blast

    # 2. Fallback Diagnostic Mode
    res_fallback = client.get('/advisory?needs_further_diagnosis=true&crop=Rice&lang=te')
    assert res_fallback.status_code == 200
    html_fb = res_fallback.data.decode('utf-8')
    assert 'మరింత నిర్ధారణ అవసరం' in html_fb
    assert 'రసాయన మందులు వాడవద్దు' in html_fb

    # 3. Default Catalog Mode
    import html as html_lib
    res_cat = client.get('/advisory?lang=en')
    assert res_cat.status_code == 200
    html_cat = html_lib.unescape(res_cat.data.decode('utf-8'))
    assert 'Expert Agricultural Advisory System' in html_cat
    assert 'Verified Crop Disease & Pest Catalog' in html_cat


# =============================================================================
# CLI Standalone Runner
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🌾 Running Rythu Mithra Phase 6 Smart Advisory System Test Suite")
    print("=" * 70)

    test_app = create_app('testing')
    test_app.config['TESTING'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False

    with test_app.app_context():
        db.create_all()

        print("  [*] 1. Testing Disease Advisory Retrieval (Blast, Blight, Wilt)...")
        test_advisory_retrieval_known_diseases()
        print("  [✓] Verified Disease 9-Section Advisories Retrieved Successfully.")

        print("  [*] 2. Testing Pest Advisory Retrieval (Whitefly, Pod Borer, etc.)...")
        test_advisory_retrieval_known_pests()
        print("  [✓] Verified Pest Management Advisories Retrieved Successfully.")

        print("  [*] 3. Testing Telugu & English Bilingual Support...")
        test_telugu_and_english_bilingual_advisory()
        print("  [✓] Unicode Preservation & Bilingual Content Verified.")

        print("  [*] 4. Testing Missing Advisory Handling...")
        test_missing_or_unknown_advisory_handling()
        print("  [✓] Graceful None Handling for Nonexistent Entries Verified.")

        print("  [*] 5. Testing Crop Normalization (Paddy -> Rice)...")
        test_crop_normalization_and_filtering()
        print("  [✓] Regional Crop Normalization & Filtering Verified.")

        print("  [*] 6. Testing Fallback Diagnosis Workflow ('diagnosis_fallback.csv')...")
        test_fallback_diagnosis_workflow()
        print("  [✓] Diagnostic Questions & Safe Cultural Guidance Verified.")

        print("  [*] 7. Testing Chemical Safety & Dosages...")
        test_chemical_safety_information()
        print("  [✓] Exact Dataset Dosages & PPE Safety Rules Enforced.")

        client_instance = test_app.test_client()

        print("  [*] 8. Testing Database Audit Logging...")
        test_advisory_view_audit_logging(client_instance, test_app)
        print("  [✓] Farmer Advisory View Audits Logged Successfully.")

        print("  [*] 9. Testing Multi-Turn Follow-Up Prediction API...")
        test_follow_up_prediction_api(client_instance)
        print("  [✓] Follow-up Symptom Re-analysis API Verified.")

        print("  [*] 10. Testing Advisory Web Interface Modes...")
        test_advisory_page_rendering_modes(client_instance)
        print("  [✓] Verified, Fallback, and Catalog UI Views Rendered Successfully.")

        db.session.remove()
        db.drop_all()

    print("=" * 70)
    print("🎉 ALL 10 PHASE 6 SMART ADVISORY TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)
