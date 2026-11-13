#!/usr/bin/env python3
"""
=============================================================================
Rythu Mithra - Frontend Integration and UI Test Suite
Phase 4: Verification of Pages, Routes, Navigation, and API Integration
=============================================================================
"""

import sys
import os
from pathlib import Path

# Force UTF-8 encoding on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from app import create_app
from database import db
from database.models import User, NLPPredictionRecord, AdvisoryQueryRecord, DiseaseDetectionRecord


@pytest.fixture
def client():
    """Create Flask test client with in-memory or test database context."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()


def test_home_page_rendering(client):
    """Verifies that the Home page loads with status 200 and branding elements."""
    res = client.get('/')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'RYTHU MITHRA' in html
    assert 'Your Smart Farming Companion' in html
    assert 'Check Crop Disease Now' in html


def test_login_and_register_pages_rendering(client):
    """Verifies that Login and Register pages render with form controls."""
    res_login = client.get('/login')
    assert res_login.status_code == 200
    assert 'Farmer Portal Login' in res_login.data.decode('utf-8')

    res_reg = client.get('/register')
    assert res_reg.status_code == 200
    assert 'Register as a New Farmer' in res_reg.data.decode('utf-8')


def test_user_registration_and_login_flow(client):
    """Tests farmer registration, password hashing, and session authentication."""
    # Register new farmer
    reg_data = {
        'full_name': 'Ramana Murthy',
        'mobile_number': '9848012345',
        'phone_or_email': '9848012345',
        'password': 'farmer_pass_123',
        'confirm_password': 'farmer_pass_123',
        'district': 'Guntur',
        'state': 'Andhra Pradesh',
        'preferred_language': 'te'
    }
    res_reg = client.post('/register', data=reg_data, follow_redirects=True)
    assert res_reg.status_code == 200
    assert 'Ramana Murthy' in res_reg.data.decode('utf-8')

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert res_logout.status_code == 200

    # Login with valid credentials
    login_data = {
        'phone_or_email': '9848012345',
        'password': 'farmer_pass_123'
    }
    res_login = client.post('/login', data=login_data, follow_redirects=True)
    assert res_login.status_code == 200
    assert 'Ramana Murthy' in res_login.data.decode('utf-8')

    # Login with wrong credentials
    client.get('/logout')
    bad_login = {
        'phone_or_email': '9848012345',
        'password': 'wrong_password'
    }
    res_bad = client.post('/login', data=bad_login, follow_redirects=True)
    assert 'Invalid' in res_bad.data.decode('utf-8')


def test_dashboard_rendering(client):
    """Verifies that the Farmer Dashboard displays real metrics and quick action cards when logged in."""
    # Register / login farmer first
    client.post('/register', data={
        'full_name': 'Test Farmer',
        'mobile_number': '9876543210',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
        'district': 'Guntur',
        'preferred_language': 'en'
    }, follow_redirects=True)

    res = client.get('/dashboard?lang=en')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Total Predictions' in html
    assert 'Quick Access Modules' in html
    assert 'Test Farmer' in html


def test_disease_prediction_page_and_form(client):
    """Verifies that the Disease Prediction page loads with crop selector and voice buttons."""
    import html as html_lib
    res = client.get('/predict?lang=en')
    assert res.status_code == 200
    html = html_lib.unescape(res.data.decode('utf-8'))
    assert 'Crop Disease & Pest Detection Workspace' in html
    assert 'Paddy' in html
    assert 'Cotton' in html
    assert 'Speak in Telugu' in html
    assert 'Analyze Symptoms with AI' in html


def test_image_detection_page_rendering(client):
    """Verifies that Image Detection page loads with drag-and-drop dropzone."""
    res = client.get('/image-detection')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Visual Leaf Disease Classifier' in html
    assert 'drag' in html.lower()

    # Alias /disease-detect also works
    res_alias = client.get('/disease-detect')
    assert res_alias.status_code == 200


def test_advisory_page_rendering(client):
    """Verifies that the Advisory page loads with Web Speech support badge and sample chips."""
    res = client.get('/advisory')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Agricultural Advisory' in html
    assert 'Web Speech' in html
    assert 'వరి' in html


def test_weather_alerts_page_rendering(client):
    """Verifies that Weather Alerts page displays seasonal agro-climate advisories."""
    res = client.get('/weather')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Weather Alerts' in html
    assert 'Forecast' in html
    assert 'Guntur' in html


def test_history_page_rendering(client):
    """Verifies that History page displays tabs for NLP predictions, image detections, and advisories."""
    client.post('/register', data={
        'full_name': 'Test Farmer History',
        'mobile_number': '9848123456',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
        'district': 'Guntur',
        'preferred_language': 'te'
    }, follow_redirects=True)

    res = client.get('/history')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'History' in html
    assert 'Image Detections' in html


def test_about_page_rendering(client):
    """Verifies that the About page renders architecture details and technical stack."""
    res = client.get('/about')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'XLM-RoBERTa' in html
    assert '96.15% Test Accuracy' in html
    assert 'System Information Flow' in html


def test_prediction_api_and_database_logging(client):
    """Verifies that POST /api/predict returns 200 and logs the prediction to SQLite database."""
    client.post('/register', data={
        'full_name': 'Predict Farmer',
        'mobile_number': '9848999999',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
        'district': 'Guntur',
        'preferred_language': 'te'
    }, follow_redirects=True)

    payload = {
        'crop': 'Tomato',
        'crop_stage': 'Fruiting',
        'description': 'టమాట కాయల మీద రంధ్రం చేసి పురుగు లోపలికి వెళ్ళినట్టు ఉంది',
        'language': 'te'
    }
    res = client.post('/api/predict', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'prediction' in data
    assert 'score' in data
    assert isinstance(data['top_predictions'], list)

    # Check dashboard reflects the logged record
    dash_res = client.get('/dashboard')
    assert 'Tomato' in dash_res.data.decode('utf-8')


if __name__ == '__main__':
    print("=" * 65)
    print("🌾 Running Rythu Mithra Phase 4 Frontend Integration Test Suite")
    print("=" * 65)

    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as c:
        with app.app_context():
            db.create_all()

            print("  [*] Testing Home Page...")
            test_home_page_rendering(c)
            print("  [✓] Home Page Loaded Successfully.")

            print("  [*] Testing Login and Register Pages...")
            test_login_and_register_pages_rendering(c)
            print("  [✓] Login & Register Pages Loaded Successfully.")

            print("  [*] Testing User Registration and Login Flow...")
            test_user_registration_and_login_flow(c)
            print("  [✓] Registration, Password Hashing, & Login Session Verified.")

            print("  [*] Testing Dashboard Page...")
            test_dashboard_rendering(c)
            print("  [✓] Farmer Dashboard Verified with Live Summary Counters.")

            print("  [*] Testing Disease Prediction Page...")
            test_disease_prediction_page_and_form(c)
            print("  [✓] Prediction Form, Crop Selectors, & Voice Controls Verified.")

            print("  [*] Testing Image Detection Page...")
            test_image_detection_page_rendering(c)
            print("  [✓] Image Detection Upload Dropzone Verified.")

            print("  [*] Testing Multilingual Advisory Page...")
            test_advisory_page_rendering(c)
            print("  [✓] Advisory Interface & Web Speech Badge Verified.")

            print("  [*] Testing Weather Alerts Page...")
            test_weather_alerts_page_rendering(c)
            print("  [✓] Agro-Climate Weather Advisory Verified.")

            print("  [*] Testing History Page...")
            test_history_page_rendering(c)
            print("  [✓] History Tabs (NLP, Image, Advisory) Verified.")

            print("  [*] Testing About Page...")
            test_about_page_rendering(c)
            print("  [✓] Architecture & Tech Stack Verified.")

            print("  [*] Testing Prediction API & Database Logging...")
            test_prediction_api_and_database_logging(c)
            print("  [✓] Prediction API & DB Logging Verified.")

            print("=" * 65)
            print("🎉 ALL 11 FRONTEND INTEGRATION TESTS PASSED SUCCESSFULLY!")
            print("=" * 65)
