"""
Security and Authentication Utilities for Rythu Mithra.
Phase 5: Secure Session Management, Route Protection, CSRF Defense, and Input Validation.
"""

import re
import secrets
import hmac
from functools import wraps
from typing import Tuple, Optional, Dict, Any
from flask import session, request, redirect, url_for, flash, jsonify, current_app


def generate_csrf_token() -> str:
    """
    Generates or retrieves a cryptographically secure CSRF token in the farmer's session.
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']


def validate_csrf_token(token: Optional[str]) -> bool:
    """
    Validates a submitted CSRF token using constant-time comparison to prevent timing attacks.
    Bypasses validation if application is in TESTING mode with CSRF disabled.
    """
    if current_app.config.get('TESTING', False) and not current_app.config.get('WTF_CSRF_ENABLED', True):
        return True
    expected = session.get('_csrf_token')
    if not expected or not token:
        return False
    return hmac.compare_digest(str(expected), str(token))


def login_required(f):
    """
    Decorator to protect routes requiring farmer authentication.
    Handles both standard browser navigation and asynchronous JSON requests.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Check if this is an API / AJAX request
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required. Please log in as a farmer to proceed.',
                    'login_required': True
                }), 401
            
            flash("Please log in to access your farmer dashboard and diagnosis history.", "info")
            return redirect(url_for('main.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def clean_mobile_number(mobile: str) -> str:
    """
    Sanitizes Indian mobile numbers by stripping spaces, hyphens, and leading +91 / 0.
    """
    if not mobile:
        return ""
    digits = re.sub(r'\D', '', mobile.strip())
    if digits.startswith('91') and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith('0') and len(digits) == 11:
        digits = digits[1:]
    return digits


def validate_mobile_number(mobile: str) -> Tuple[bool, str]:
    """
    Validates that a mobile number is a valid 10-digit Indian telecom number starting with 6, 7, 8, or 9.
    """
    cleaned = clean_mobile_number(mobile)
    if not cleaned:
        return False, "Mobile number is required."
    if not re.match(r'^[6-9]\d{9}$', cleaned):
        return False, "Please enter a valid 10-digit Indian mobile number (starts with 6-9)."
    return True, cleaned


def validate_email_address(email: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validates optional email address format.
    """
    if not email or not email.strip():
        return True, None  # Email is optional
    cleaned = email.strip().lower()
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, cleaned):
        return False, "Please enter a valid email address."
    return True, cleaned


def validate_farmer_registration(data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Comprehensive input validation for farmer registration.
    Returns (is_valid, error_message, cleaned_data).
    """
    full_name = (data.get('full_name') or '').strip()
    mobile = (data.get('mobile_number') or data.get('phone_or_email') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    confirm_password = data.get('confirm_password') or ''
    state = (data.get('state') or 'Andhra Pradesh').strip()
    district = (data.get('district') or 'Guntur').strip()
    mandal = (data.get('mandal') or '').strip()
    preferred_language = (data.get('preferred_language') or 'te').strip()

    if not full_name or len(full_name) < 2:
        return False, "Full name must be at least 2 characters.", {}

    # Validate mobile
    is_valid_mobile, mobile_res = validate_mobile_number(mobile)
    if not is_valid_mobile:
        return False, mobile_res, {}

    # Validate email (optional)
    is_valid_email, email_res = validate_email_address(email)
    if not is_valid_email:
        return False, email_res, {}

    # Validate password
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters long.", {}

    if confirm_password and password != confirm_password:
        return False, "Password and confirm password do not match.", {}

    if preferred_language not in ['te', 'en']:
        preferred_language = 'te'

    cleaned = {
        'full_name': full_name,
        'mobile_number': mobile_res,
        'email': email_res,
        'password': password,
        'state': state or 'Andhra Pradesh',
        'district': district or 'Guntur',
        'mandal': mandal,
        'preferred_language': preferred_language
    }
    return True, None, cleaned
