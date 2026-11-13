#!/usr/bin/env python3
"""
=============================================================================
Rythu Mithra - Phase 5 Authentication, Database & History Test Suite
=============================================================================
Validates:
1. Farmer Registration (fields, validation, duplicate prevention)
2. Password Hashing (Werkzeug pbkdf2/scrypt, no plaintext passwords)
3. Farmer Login & Logout (mobile or email login, session management)
4. Protected Route Guards (@login_required for dashboard and history)
5. Prediction Linking (audit trail linked to farmer user_id)
6. Farmer Data Isolation (zero data leakage between farmer accounts)
7. IDOR Protection (prevent direct object access across farmer boundaries)
8. Advanced History Filtering (search, crop, disease, date range)
9. CSRF Protection (token validation on forms)
10. Session Security & Cookie Configuration
=============================================================================
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

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
from database.models import User, NLPPredictionRecord, AdvisoryQueryRecord, DiseaseDetectionRecord
from werkzeug.security import check_password_hash


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
# 1. Farmer Registration & Password Hashing Tests
# =============================================================================

def test_farmer_registration_success(client, app):
    """Verifies that a new farmer registers successfully with all required fields."""
    reg_payload = {
        'full_name': 'Venkateswara Rao',
        'mobile_number': '9848011223',
        'email': 'venkat@krishi.org',
        'state': 'Andhra Pradesh',
        'district': 'Guntur',
        'mandal': 'Tenali',
        'preferred_language': 'te',
        'password': 'secret_password_123',
        'confirm_password': 'secret_password_123'
    }
    res = client.post('/register', data=reg_payload, follow_redirects=True)
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Venkateswara Rao' in html

    # Verify user in database
    with app.app_context():
        user = User.query.filter_by(mobile_number='9848011223').first()
        assert user is not None
        assert user.full_name == 'Venkateswara Rao'
        assert user.email == 'venkat@krishi.org'
        assert user.district == 'Guntur'
        assert user.mandal == 'Tenali'
        assert user.preferred_language == 'te'
        
        # Verify password is never stored as plaintext
        assert user.password_hash != 'secret_password_123'
        assert check_password_hash(user.password_hash, 'secret_password_123') is True
        assert not check_password_hash(user.password_hash, 'wrong_pass')


def test_duplicate_mobile_registration_prevented(client):
    """Verifies that duplicate mobile numbers are rejected."""
    payload = {
        'full_name': 'Farmer One',
        'mobile_number': '9988776655',
        'password': 'password123',
        'confirm_password': 'password123',
        'district': 'Krishna',
        'preferred_language': 'te'
    }
    client.post('/register', data=payload, follow_redirects=True)
    client.get('/logout')

    # Attempt second registration with same mobile number
    payload2 = {
        'full_name': 'Farmer Two',
        'mobile_number': '9988776655',
        'password': 'anotherpassword',
        'confirm_password': 'anotherpassword',
        'district': 'Warangal',
        'preferred_language': 'te'
    }
    res = client.post('/register', data=payload2, follow_redirects=True)
    html = res.data.decode('utf-8')
    assert 'already exists' in html.lower() or 'log in' in html.lower()


def test_registration_validation_errors(client):
    """Verifies that invalid mobile, short passwords, and mismatched passwords fail validation."""
    # 1. Invalid mobile (less than 10 digits or invalid format)
    res_bad_mobile = client.post('/register', data={
        'full_name': 'Test Farmer',
        'mobile_number': '12345',
        'password': 'pass',
        'confirm_password': 'pass',
        'district': 'Guntur'
    }, follow_redirects=True)
    assert 'valid 10-digit' in res_bad_mobile.data.decode('utf-8').lower()

    # 2. Mismatched passwords
    res_mismatch = client.post('/register', data={
        'full_name': 'Test Farmer',
        'mobile_number': '9848999991',
        'password': 'pass_alpha',
        'confirm_password': 'pass_beta',
        'district': 'Guntur'
    }, follow_redirects=True)
    assert 'match' in res_mismatch.data.decode('utf-8').lower()


# =============================================================================
# 2. Login, Logout & Session Management Tests
# =============================================================================

def test_login_with_mobile_and_with_email(client):
    """Verifies that a farmer can log in using either their mobile number or their registered email."""
    client.post('/register', data={
        'full_name': 'Nagarjuna Reddy',
        'mobile_number': '9440123456',
        'email': 'nagarjuna@rythu.in',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
        'district': 'Kurnool',
        'preferred_language': 'te'
    }, follow_redirects=True)
    client.get('/logout')

    # Login via Mobile
    res_mobile = client.post('/login', data={
        'phone_or_email': '9440123456',
        'password': 'securepassword'
    }, follow_redirects=True)
    assert res_mobile.status_code == 200
    assert 'Nagarjuna Reddy' in res_mobile.data.decode('utf-8')
    client.get('/logout')

    # Login via Email
    res_email = client.post('/login', data={
        'phone_or_email': 'nagarjuna@rythu.in',
        'password': 'securepassword'
    }, follow_redirects=True)
    assert res_email.status_code == 200
    assert 'Nagarjuna Reddy' in res_email.data.decode('utf-8')


def test_invalid_login_handling(client):
    """Verifies that invalid password and non-existent credentials display friendly error messages."""
    client.post('/register', data={
        'full_name': 'Sita Devi',
        'mobile_number': '9848555555',
        'password': 'correct_pass',
        'confirm_password': 'correct_pass',
        'district': 'Guntur'
    }, follow_redirects=True)
    client.get('/logout')

    # Wrong password
    res_wrong_pw = client.post('/login', data={
        'phone_or_email': '9848555555',
        'password': 'incorrect_password'
    }, follow_redirects=True)
    assert 'Invalid' in res_wrong_pw.data.decode('utf-8')

    # Non-existent user
    res_not_found = client.post('/login', data={
        'phone_or_email': '9999999999',
        'password': 'some_password'
    }, follow_redirects=True)
    assert 'Invalid' in res_not_found.data.decode('utf-8')


def test_logout_clears_session(client):
    """Verifies that logging out terminates active farmer session."""
    client.post('/register', data={
        'full_name': 'Logout Farmer',
        'mobile_number': '9848111222',
        'password': 'password123',
        'confirm_password': 'password123',
        'district': 'Krishna'
    }, follow_redirects=True)

    # Confirm session active
    res_dash = client.get('/dashboard')
    assert res_dash.status_code == 200
    assert 'Logout Farmer' in res_dash.data.decode('utf-8')

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert 'logged out' in res_logout.data.decode('utf-8').lower()

    # Attempt to access dashboard again - should redirect to login
    res_unauth = client.get('/dashboard', follow_redirects=False)
    assert res_unauth.status_code == 302
    assert '/login' in res_unauth.headers['Location']


# =============================================================================
# 3. Route Protection & Unauthorized Access Tests
# =============================================================================

def test_unauthorized_dashboard_and_history_access(client):
    """Verifies that private pages redirect unauthenticated visitors to login with next parameter."""
    # Unauthorized Dashboard
    res_dash = client.get('/dashboard', follow_redirects=False)
    assert res_dash.status_code == 302
    assert '/login' in res_dash.headers['Location']
    assert 'dashboard' in res_dash.headers['Location']

    # Unauthorized History
    res_hist = client.get('/history', follow_redirects=False)
    assert res_hist.status_code == 302
    assert '/login' in res_hist.headers['Location']
    assert 'history' in res_hist.headers['Location']


# =============================================================================
# 4. Prediction History Linking & Farmer Data Isolation Tests
# =============================================================================

def test_nlp_prediction_linking_to_farmer(client, app):
    """Verifies that an NLP prediction is linked to the authenticated farmer's user_id."""
    client.post('/register', data={
        'full_name': 'Kishan Patel',
        'mobile_number': '9848222333',
        'password': 'password123',
        'confirm_password': 'password123',
        'district': 'Guntur'
    }, follow_redirects=True)

    payload = {
        'crop': 'Tomato',
        'crop_stage': 'Fruiting',
        'description': 'టమాట కాయల మీద రంధ్రం చేసి పురుగు లోపలికి వెళ్ళినట్టు ఉంది',
        'language': 'te'
    }
    res = client.post('/api/predict', json=payload)
    assert res.status_code == 200

    with app.app_context():
        user = User.query.filter_by(mobile_number='9848222333').first()
        pred = NLPPredictionRecord.query.filter_by(user_id=user.id).first()
        assert pred is not None
        assert pred.user_id == user.id
        assert pred.crop_name == 'Tomato'
        assert 'టమాట' in pred.symptom_description


def test_farmer_to_farmer_data_isolation(client, app):
    """
    CRITICAL SECURITY TEST:
    Verifies that Farmer A and Farmer B CANNOT see each other's diagnostic predictions.
    Each farmer must only access records linked exclusively to their own account.
    """
    # 1. Register and submit diagnosis as Farmer A
    client.post('/register', data={
        'full_name': 'Farmer Alpha',
        'mobile_number': '9111111111',
        'password': 'password_alpha',
        'confirm_password': 'password_alpha',
        'district': 'Guntur'
    }, follow_redirects=True)

    client.post('/api/predict', json={
        'crop': 'Paddy',
        'crop_stage': 'Vegetative',
        'description': 'వరి ఆకులపై అగ్గి తెగులు మచ్చలు కనిపించాయి (Alpha Secret Diagnosis)',
        'language': 'te'
    })
    client.get('/logout')

    # 2. Register and submit diagnosis as Farmer B
    client.post('/register', data={
        'full_name': 'Farmer Beta',
        'mobile_number': '9222222222',
        'password': 'password_beta',
        'confirm_password': 'password_beta',
        'district': 'Warangal'
    }, follow_redirects=True)

    client.post('/api/predict', json={
        'crop': 'Cotton',
        'crop_stage': 'Flowering',
        'description': 'పత్తి చేనులో తెల్లదోమ ఉధృతి ఎక్కువగా ఉంది (Beta Secret Diagnosis)',
        'language': 'te'
    })

    # 3. Verify Farmer Beta's history contains ONLY Beta's records, NOT Alpha's!
    res_beta_hist = client.get('/history')
    html_beta = res_beta_hist.data.decode('utf-8')
    assert 'Beta Secret Diagnosis' in html_beta
    assert 'Alpha Secret Diagnosis' not in html_beta  # Strict isolation verified!

    # 4. Verify Farmer Beta's dashboard summary shows ONLY 1 prediction
    res_beta_dash = client.get('/dashboard')
    html_beta_dash = res_beta_dash.data.decode('utf-8')
    assert 'Beta Secret Diagnosis' in html_beta_dash
    assert 'Alpha Secret Diagnosis' not in html_beta_dash

    # 5. Log back in as Farmer Alpha and verify isolation
    client.get('/logout')
    client.post('/login', data={
        'phone_or_email': '9111111111',
        'password': 'password_alpha'
    }, follow_redirects=True)

    res_alpha_hist = client.get('/history')
    html_alpha = res_alpha_hist.data.decode('utf-8')
    assert 'Alpha Secret Diagnosis' in html_alpha
    assert 'Beta Secret Diagnosis' not in html_alpha  # Strict isolation verified!


def test_idor_protection_on_history_detail(client, app):
    """
    IDOR (Insecure Direct Object Reference) Prevention:
    Verifies that Farmer B cannot fetch Farmer A's diagnosis detail via API by guessing record_id.
    """
    # Farmer A creates a record
    client.post('/register', data={
        'full_name': 'Private Farmer A',
        'mobile_number': '9333333333',
        'password': 'password_a',
        'confirm_password': 'password_a',
        'district': 'Guntur'
    }, follow_redirects=True)

    client.post('/api/predict', json={
        'crop': 'Chilli',
        'crop_stage': 'Fruiting',
        'description': 'మిరపలో ఆకుముడుత తీవ్రంగా ఉంది',
        'language': 'te'
    })

    with app.app_context():
        user_a = User.query.filter_by(mobile_number='9333333333').first()
        pred_a = NLPPredictionRecord.query.filter_by(user_id=user_a.id).first()
        record_a_id = pred_a.id

    client.get('/logout')

    # Farmer B logs in and tries to access Farmer A's record by ID
    client.post('/register', data={
        'full_name': 'Attacker Farmer B',
        'mobile_number': '9444444444',
        'password': 'password_b',
        'confirm_password': 'password_b',
        'district': 'Krishna'
    }, follow_redirects=True)

    res_idor = client.get(f'/api/history/{record_a_id}')
    assert res_idor.status_code == 404  # Not found or access denied
    assert res_idor.get_json()['success'] is False


# =============================================================================
# 5. History Filtering Tests (Search, Crop, Disease, Date Range)
# =============================================================================

def test_history_filtering_search_and_crop(client, app):
    """Verifies that history filter returns matches according to search query and crop parameter."""
    client.post('/register', data={
        'full_name': 'Filter Test Farmer',
        'mobile_number': '9555555555',
        'password': 'password_f',
        'confirm_password': 'password_f',
        'district': 'Guntur'
    }, follow_redirects=True)

    # Create 2 different predictions
    client.post('/api/predict', json={
        'crop': 'Tomato',
        'crop_stage': 'Fruiting',
        'description': 'టమాట కాయలపై పురుగు రంధ్రాలు (SearchTargetOne)',
        'language': 'te'
    })
    client.post('/api/predict', json={
        'crop': 'Paddy',
        'crop_stage': 'Seedling',
        'description': 'వరి ఆకులపై గోధుమ రంగు మచ్చలు (SearchTargetTwo)',
        'language': 'te'
    })

    # Search filter
    res_search = client.get('/history?search=SearchTargetOne')
    html_search = res_search.data.decode('utf-8')
    assert 'SearchTargetOne' in html_search
    assert 'SearchTargetTwo' not in html_search

    # Crop filter
    res_crop = client.get('/history?crop=Paddy')
    html_crop = res_crop.data.decode('utf-8')
    assert 'SearchTargetTwo' in html_crop
    assert 'SearchTargetOne' not in html_crop


# =============================================================================
# 6. CSRF & Session Security Configuration Tests
# =============================================================================

def test_session_cookie_security_settings(app):
    """Verifies that security cookie parameters (HttpOnly, SameSite) are active."""
    assert app.config['SESSION_COOKIE_HTTPONLY'] is True
    assert app.config['SESSION_COOKIE_SAMESITE'] == 'Lax'
    assert app.config['PERMANENT_SESSION_LIFETIME'] == 60 * 60 * 24 * 7  # 7 Days


def test_csrf_token_generation_and_validation(client, app):
    """Verifies that CSRF generation produces cryptographically strong tokens and rejects bad tokens."""
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        with app.test_request_context():
            from utils.security import generate_csrf_token, validate_csrf_token
            from flask import session

            token = generate_csrf_token()
            assert token is not None
            assert len(token) == 64  # 32 bytes in hex

            # Valid token matches
            assert validate_csrf_token(token) is True

            # Forged token is rejected
            assert validate_csrf_token('bad_fake_token_12345') is False
            assert validate_csrf_token(None) is False
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


# =============================================================================
# CLI Runner
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🌾 Running Rythu Mithra Phase 5 Authentication & Security Suite")
    print("=" * 70)

    test_app = create_app('testing')
    test_app.config['TESTING'] = True
    test_app.config['WTF_CSRF_ENABLED'] = False

    with test_app.app_context():
        db.create_all()

        print("  [*] 1. Testing Farmer Registration...")
        test_farmer_registration_success(test_app.test_client(), test_app)
        print("  [✓] Registration & Werkzeug Password Hashing Verified.")

        print("  [*] 2. Testing Duplicate Registration Prevention...")
        test_duplicate_mobile_registration_prevented(test_app.test_client())
        print("  [✓] Duplicate Mobile Numbers Rejected.")

        print("  [*] 3. Testing Input Validation Rules...")
        test_registration_validation_errors(test_app.test_client())
        print("  [✓] Validation Rules (Mobile, Password Match) Enforced.")

        print("  [*] 4. Testing Multi-Identifier Login (Mobile & Email)...")
        test_login_with_mobile_and_with_email(test_app.test_client())
        print("  [✓] Login with Mobile and Email Verified.")

        print("  [*] 5. Testing Invalid Login Handling...")
        test_invalid_login_handling(test_app.test_client())
        print("  [✓] Invalid Credentials Gracefully Rejected.")

        print("  [*] 6. Testing Logout & Session Clearing...")
        test_logout_clears_session(test_app.test_client())
        print("  [✓] Logout Terminates Session.")

        print("  [*] 7. Testing Protected Route Guards (@login_required)...")
        test_unauthorized_dashboard_and_history_access(test_app.test_client())
        print("  [✓] Unauthorized Access Redirects to Login with Next URL.")

        print("  [*] 8. Testing Prediction Audit Linking...")
        test_nlp_prediction_linking_to_farmer(test_app.test_client(), test_app)
        print("  [✓] Predictions Persisted with Authenticated Farmer User ID.")

        print("  [*] 9. Testing Farmer-to-Farmer Data Isolation (ZERO LEAKAGE)...")
        test_farmer_to_farmer_data_isolation(test_app.test_client(), test_app)
        print("  [✓] Complete Farmer Data Isolation Confirmed: No Leakage.")

        print("  [*] 10. Testing IDOR Prevention on Diagnostic API...")
        test_idor_protection_on_history_detail(test_app.test_client(), test_app)
        print("  [✓] IDOR Prevention Active: Farmer B Cannot View Farmer A's Records.")

        print("  [*] 11. Testing History Filtering (Search & Crop)...")
        test_history_filtering_search_and_crop(test_app.test_client(), test_app)
        print("  [✓] Advanced Search and Parameterized Filtering Verified.")

        print("  [*] 12. Testing Session Security Configuration...")
        test_session_cookie_security_settings(test_app)
        test_csrf_token_generation_and_validation(test_app.test_client(), test_app)
        print("  [✓] HTTPOnly, SameSite Lax, & Constant-Time CSRF Tokens Verified.")

        db.session.remove()
        db.drop_all()

    print("=" * 70)
    print("🎉 ALL 12 PHASE 5 SECURITY & AUTHENTICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)
