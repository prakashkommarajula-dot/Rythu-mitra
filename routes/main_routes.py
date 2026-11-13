"""
Main Blueprint for Rythu Mithra.
Phase 5: Secure Farmer Authentication, Profile Management, Isolated Prediction History, and Dashboard.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from database import db
from database.models import User
from utils.security import (
    login_required,
    generate_csrf_token,
    validate_csrf_token,
    validate_farmer_registration,
    clean_mobile_number
)
from services.history_service import (
    get_recent_detections,
    get_recent_advisories,
    get_recent_nlp_predictions,
    get_prediction_by_id,
    get_dashboard_summary
)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Renders the modern home / landing page with hero, features, and quick CTA."""
    # If user is logged in, show their summary; otherwise show platform totals
    user_id = session.get('user_id')
    summary = get_dashboard_summary(user_id=user_id)
    return render_template('index.html', summary=summary)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the farmer dashboard with live prediction counts, recent history, and quick action shortcuts.
    Strictly isolated to the authenticated farmer's real records.
    """
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        session.clear()
        flash("Farmer profile not found. Please log in again.", "warning")
        return redirect(url_for('main.login'))

    # Load authentic metrics and history strictly for this farmer
    summary = get_dashboard_summary(user_id=user_id)
    recent_nlp = get_recent_nlp_predictions(user_id=user_id, limit=5)
    recent_detections = get_recent_detections(user_id=user_id, limit=5)
    recent_advisories = get_recent_advisories(user_id=user_id, limit=5)

    return render_template(
        'dashboard.html',
        user=user,
        summary=summary,
        recent_nlp=recent_nlp,
        recent_detections=recent_detections,
        recent_advisories=recent_advisories,
        user_name=user.full_name
    )


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles farmer login via mobile number or email and password."""
    # If already authenticated, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    next_url = request.args.get('next') or url_for('main.dashboard')

    if request.method == 'POST':
        # CSRF Validation
        submitted_token = request.form.get('csrf_token')
        if not validate_csrf_token(submitted_token):
            flash("Security validation failed (CSRF token invalid or expired). Please try again.", "danger")
            return render_template('login.html', next=next_url)

        identifier = request.form.get('phone_or_email', '').strip()
        password = request.form.get('password', '').strip()

        if not identifier or not password:
            flash("Please enter both your mobile number/email and password.", "danger")
            return render_template('login.html', identifier=identifier, next=next_url)

        # Allow login via cleaned 10-digit mobile number OR email OR phone_or_email
        cleaned_mobile = clean_mobile_number(identifier)
        user = User.query.filter(
            (User.mobile_number == cleaned_mobile) |
            (User.email == identifier.lower()) |
            (User.phone_or_email == identifier)
        ).first()

        if user and user.check_password(password):
            # Establish secure session
            session.clear()
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['user_mobile'] = user.mobile_number or user.phone_or_email
            session['user_email'] = user.email
            session['user_district'] = user.district
            session['user_mandal'] = user.mandal or ''
            session['user_state'] = user.state or 'Andhra Pradesh'
            session['user_language'] = user.preferred_language or 'te'
            session.permanent = True

            flash(f"నమస్కారం / Welcome back, {user.full_name}!", "success")
            
            # Safe redirection
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid mobile number/email or password. Please verify and try again.", "danger")
            return render_template('login.html', identifier=identifier, next=next_url)

    return render_template('login.html', next=next_url)


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new farmer account registration with input validation and duplicate prevention."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        # CSRF Validation
        submitted_token = request.form.get('csrf_token')
        if not validate_csrf_token(submitted_token):
            flash("Security validation failed (CSRF token invalid or expired). Please try again.", "danger")
            return render_template('register.html', form_data=request.form)

        # Comprehensive input validation
        is_valid, error_msg, cleaned = validate_farmer_registration(request.form)
        if not is_valid:
            flash(error_msg, "danger")
            return render_template('register.html', form_data=request.form)

        # Check for duplicate mobile number
        existing_mobile = User.query.filter(
            (User.mobile_number == cleaned['mobile_number']) |
            (User.phone_or_email == cleaned['mobile_number'])
        ).first()
        if existing_mobile:
            flash("An account with this mobile number already exists. Please log in instead.", "warning")
            return redirect(url_for('main.login'))

        # Check for duplicate email if email was provided
        if cleaned['email']:
            existing_email = User.query.filter_by(email=cleaned['email']).first()
            if existing_email:
                flash("An account with this email address already exists. Please log in instead.", "warning")
                return redirect(url_for('main.login'))

        try:
            new_user = User(
                full_name=cleaned['full_name'],
                mobile_number=cleaned['mobile_number'],
                email=cleaned['email'],
                phone_or_email=cleaned['mobile_number'],
                state=cleaned['state'],
                district=cleaned['district'],
                mandal=cleaned['mandal'],
                preferred_language=cleaned['preferred_language']
            )
            new_user.set_password(cleaned['password'])
            db.session.add(new_user)
            db.session.commit()

            # Auto-login new user
            session.clear()
            session['user_id'] = new_user.id
            session['user_name'] = new_user.full_name
            session['user_mobile'] = new_user.mobile_number
            session['user_email'] = new_user.email
            session['user_district'] = new_user.district
            session['user_mandal'] = new_user.mandal or ''
            session['user_state'] = new_user.state or 'Andhra Pradesh'
            session['user_language'] = new_user.preferred_language or 'te'
            session.permanent = True

            flash("ఖాతా విజయవంతంగా సృష్టించబడింది! Welcome to Rythu Mithra.", "success")
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error during registration: {e}")
            flash("Registration could not be completed due to a server error. Please try again.", "danger")
            return render_template('register.html', form_data=request.form)

    return render_template('register.html')


@main_bp.route('/logout')
def logout():
    """Logs out current farmer and clears active session."""
    session.clear()
    flash("మీరు విజయవంతంగా లాగౌట్ అయ్యారు / You have been logged out successfully.", "info")
    return redirect(url_for('main.index'))


@main_bp.route('/history')
@login_required
def history():
    """
    Renders the comprehensive history page with tabs for NLP predictions, image detections, and advisories.
    Strictly isolated to the logged-in farmer with real-time server-side and client-side filtering.
    """
    user_id = session['user_id']
    search = request.args.get('search', '').strip()
    crop = request.args.get('crop', '').strip()
    disease = request.args.get('disease', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    nlp_predictions = get_recent_nlp_predictions(
        user_id=user_id,
        limit=100,
        crop=crop,
        disease=disease,
        search=search,
        date_from=date_from,
        date_to=date_to
    )
    image_detections = get_recent_detections(user_id=user_id, limit=50)
    advisories = get_recent_advisories(user_id=user_id, limit=50)

    # Distinct crops and diseases for filter dropdowns
    available_crops = sorted(list({p['crop_name'] for p in nlp_predictions if p.get('crop_name')}))
    available_diseases = sorted(list({p['detected_disease'] for p in nlp_predictions if p.get('detected_disease')}))

    return render_template(
        'history.html',
        nlp_predictions=nlp_predictions,
        image_detections=image_detections,
        advisories=advisories,
        available_crops=available_crops,
        available_diseases=available_diseases,
        filters={
            'search': search,
            'crop': crop,
            'disease': disease,
            'date_from': date_from,
            'date_to': date_to
        }
    )


@main_bp.route('/api/history/<int:record_id>', methods=['GET'])
@login_required
def get_history_detail(record_id):
    """
    Retrieves full details of a single NLP diagnosis record.
    Enforces IDOR prevention: only returns record if it belongs to the authenticated farmer.
    """
    user_id = session['user_id']
    record = get_prediction_by_id(prediction_id=record_id, user_id=user_id)
    if not record:
        return jsonify({
            'success': False,
            'error': 'Diagnosis record not found or access denied.'
        }), 404

    return jsonify({
        'success': True,
        'record': record
    }), 200


@main_bp.route('/weather')
def weather():
    """Renders real agricultural weather advisory and climate alerts for AP & Telangana farmers."""
    return render_template('weather.html')


@main_bp.route('/about')
def about():
    """Renders system architecture, XLM-RoBERTa model specs, team, and project information."""
    return render_template('about.html')
