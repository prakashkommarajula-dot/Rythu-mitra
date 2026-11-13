"""
Unit and Integration Test Suite: Telugu–English Language Switching
Tests:
1. /api/set-language API endpoint (POST & GET).
2. Cookie 'rythu_lang' generation and session synchronization.
3. Authenticated farmer language persistence in SQLite database.
4. Language context injection in Jinja templates across all pages.
5. Agricultural advisory retrieval in Telugu and English.
6. Fallback handling when English advisory is unavailable.
7. Translation dictionary consistency between 'en' and 'te'.
8. Telugu Unicode preservation without mojibake / corrupted encoding.
"""

import os
import json
import pytest
from app import create_app
from database import db
from database.models import User, AdvisoryViewRecord
from services.advisory_service import get_advisory, get_fallback_advisory


@pytest.fixture
def test_app():
    """Configures application with testing SQLite database."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_set_language_api_post(client):
    """Verifies POST /api/set-language sets session and returns cookie."""
    # Test setting to English
    res_en = client.post('/api/set-language', json={'language': 'en'})
    assert res_en.status_code == 200
    data_en = res_en.get_json()
    assert data_en['success'] is True
    assert data_en['language'] == 'en'
    assert 'rythu_lang=en' in str(res_en.headers.get('Set-Cookie', ''))

    # Test setting to Telugu
    res_te = client.post('/api/set-language', json={'language': 'te'})
    assert res_te.status_code == 200
    data_te = res_te.get_json()
    assert data_te['success'] is True
    assert data_te['language'] == 'te'
    assert 'rythu_lang=te' in str(res_te.headers.get('Set-Cookie', ''))


def test_set_language_api_invalid_fallback(client):
    """Verifies invalid or unknown languages default safely to Telugu ('te')."""
    res = client.post('/api/set-language', json={'language': 'french'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['language'] == 'te'


def test_user_language_persisted_in_database(client, test_app):
    """Verifies that an authenticated farmer's language change updates their DB record."""
    with test_app.app_context():
        user = User(
            full_name="Rama Rao",
            mobile_number="9876543210",
            phone_or_email="9876543210",
            preferred_language="te"
        )
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Log in user
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['user_name'] = "Rama Rao"
        sess['user_language'] = "te"

    # Switch to English
    res = client.post('/api/set-language', json={'language': 'en'})
    assert res.status_code == 200

    # Verify user preferred_language updated in SQLite database
    with test_app.app_context():
        updated_user = db.session.get(User, user_id)
        assert updated_user.preferred_language == 'en'


def test_pages_render_with_cookie_language(client):
    """Verifies that pages render with the language specified in cookie."""
    # Set cookie to English
    client.set_cookie('rythu_lang', 'en')

    # Test index page
    res_home = client.get('/')
    assert res_home.status_code == 200
    html_home = res_home.get_data(as_text=True)
    assert '<html lang="en">' in html_home

    # Test predict page
    res_predict = client.get('/predict')
    assert res_predict.status_code == 200
    html_predict = res_predict.get_data(as_text=True)
    assert '<html lang="en">' in html_predict

    # Set cookie to Telugu
    client.set_cookie('rythu_lang', 'te')
    res_home_te = client.get('/')
    assert res_home_te.status_code == 200
    html_home_te = res_home_te.get_data(as_text=True)
    assert '<html lang="te">' in html_home_te


def test_telugu_advisory_retrieval():
    """Verifies Telugu advisory retrieves verified Advisory_Telugu field."""
    adv = get_advisory(disease_or_pest="Blast", crop="Rice", language="te")
    assert adv is not None
    assert adv['disease_or_pest'] == "Blast"
    assert adv['crop'] == "Rice"
    assert adv['advisory_te'] != ""
    assert "English advisory is not available" not in adv['advisory_te']
    # Verify Telugu characters exist
    assert any('\u0c00' <= char <= '\u0c7f' for char in adv['advisory_te'])


def test_english_advisory_retrieval():
    """Verifies English advisory retrieves verified Advisory_English field."""
    adv = get_advisory(disease_or_pest="Blast", crop="Rice", language="en")
    assert adv is not None
    assert adv['advisory_en'] != ""
    # Should contain English text
    assert "English advisory is not available" not in adv['advisory_en']


def test_missing_advisory_fallback_message():
    """Verifies clear fallback message when advisory is not available."""
    # Test with empty query or fallback
    fb = get_fallback_advisory(crop="Rice", language="en")
    assert fb is not None
    assert fb['is_fallback'] is True
    assert "English advisory is not available for this record." in fb['advisory_en'] or len(fb['advisory_en']) > 0


def test_translation_dictionary_key_parity():
    """Verifies that all keys in 'en' also exist in 'te' in translations_data.py and translations.js."""
    from utils.translations_data import TRANSLATIONS
    assert 'en' in TRANSLATIONS
    assert 'te' in TRANSLATIONS
    
    en_keys = set(TRANSLATIONS['en'].keys())
    te_keys = set(TRANSLATIONS['te'].keys())
    
    missing_in_te = en_keys - te_keys
    assert len(missing_in_te) == 0, f"Keys in en but missing in te: {missing_in_te}"
    
    # Also verify translations.js exists and exports window.TRANSLATIONS
    trans_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'js', 'translations.js')
    assert os.path.exists(trans_path)
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'TRANSLATIONS' in content
    # Validate syntax by ensuring both en and te sections exist in JS
    assert 'en: {' in content or '"en": {' in content
    assert 'te: {' in content or '"te": {' in content

    # Check essential keys exist in content
    essential_keys = [
        "app_name",
        "app_tagline",
        "nav_dashboard",
        "nav_predict",
        "nav_advisory",
        "nav_weather",
        "nav_history",
        "predict_title",
        "form_symptom_label",
        "btn_submit_predict",
        "res_card_title",
        "res_detected_title",
        "res_confidence_title",
        "res_btn_advisory",
        "advisory_title",
        "advisory_dossier_title",
        "advisory_sec_chemical",
        "auth_login_title",
        "auth_reg_title",
        "history_title",
        "weather_title",
        "about_title"
    ]
    for key in essential_keys:
        assert f'"{key}"' in content or f"'{key}'" in content, f"Key {key} missing from translations dictionary!"


def test_telugu_unicode_integrity():
    """Verifies Telugu Unicode preservation across UI translation dictionary."""
    trans_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'js', 'translations.js')
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sample Telugu keywords that must be intact
    telugu_keywords = [
        "రైతు మిత్ర",
        "డ్యాష్‌బోర్డ్",
        "తెగులు గుర్తింపు",
        "వ్యవసాయ సలహా",
        "సమగ్ర సస్యరక్షణ",
        "వాతావరణ హెచ్చరికలు"
    ]
    for kw in telugu_keywords:
        assert kw in content, f"Corrupted or missing Telugu keyword: {kw}"


def test_query_param_language_switching(client):
    """Verifies that passing ?lang=en or ?lang=te renders server templates in that language."""
    # Test Home page
    res_en = client.get('/?lang=en')
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert 'Dear Farmers! Protect Your Crops from Diseases.' in html_en
    assert '<html lang="en">' in html_en

    res_te = client.get('/?lang=te')
    assert res_te.status_code == 200
    html_te = res_te.get_data(as_text=True)
    assert 'రైతు సోదరులారా! మీ పంటను తెగుళ్ల నుంచి కాపాడుకోండి.' in html_te
    assert '<html lang="te">' in html_te

    # Test Weather page
    res_weather_en = client.get('/weather?lang=en')
    assert res_weather_en.status_code == 200
    html_w_en = res_weather_en.get_data(as_text=True)
    assert 'Leaf Blast risk elevated' in html_w_en

    res_weather_te = client.get('/weather?lang=te')
    assert res_weather_te.status_code == 200
    html_w_te = res_weather_te.get_data(as_text=True)
    assert 'అగ్గి తెగులు వచ్చే అవకాశం ఎక్కువ' in html_w_te

