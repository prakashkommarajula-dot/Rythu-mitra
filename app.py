"""
Rythu Mithra (రైతు మిత్ర)
AI-Based Multilingual Crop Disease and Pest Detection and Agricultural Advisory System
Main Application Entry Point and Application Factory
"""

import os
import sys

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, render_template, jsonify, request, session, make_response, redirect, url_for
from config import config_by_name, DevelopmentConfig
from database import init_db, db
from database.models import User
from utils.translations import get_translation
from routes import main_bp, disease_bp, advisory_bp
from utils.logger import setup_logger
from utils.security import generate_csrf_token

logger = setup_logger()


def create_app(config_name=None):
    """
    Application Factory for Rythu Mithra.
    Initializes Flask, binds database, registers modular blueprints and error handlers.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    config_class = config_by_name.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize SQLite Database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(disease_bp)
    app.register_blueprint(advisory_bp)

    # Before request to capture and sync URL lang parameter, cookie, and session
    @app.before_request
    def set_request_language():
        lang = request.args.get('lang') or request.cookies.get('rythu_lang') or session.get('user_language') or 'en'
        lang = str(lang).lower().strip()
        if lang not in ['te', 'en']:
            lang = 'en'
        session['user_language'] = lang

    # Context processor to inject global variables into Jinja2 templates
    @app.context_processor
    def inject_globals():
        lang = request.args.get('lang') or request.cookies.get('rythu_lang') or session.get('user_language') or 'en'
        lang = str(lang).lower().strip()
        if lang not in ['te', 'en']:
            lang = 'en'

        def t(key, fallback=None):
            return get_translation(key, lang=lang, fallback=fallback)

        return {
            'app_name': 'RYTHU MITHRA' if lang == 'en' else 'రైతు మిత్ర (RYTHU MITHRA)',
            'app_tagline': t('app_tagline', 'Your Smart Farming Companion' if lang == 'en' else 'మీ నమ్మకమైన వ్యవసాయ సహచరి'),
            'supported_languages': app.config.get('SUPPORTED_LANGUAGES', {}),
            'current_lang': lang,
            't': t,
            'csrf_token': generate_csrf_token
        }

    # Disable caching for HTML and dynamic scripts, and ensure active language cookie is set on every response
    @app.after_request
    def add_cache_headers(response):
        if request.path.startswith('/static/js/') or (response.content_type and 'text/html' in response.content_type):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'

        lang = request.args.get('lang') or request.cookies.get('rythu_lang') or session.get('user_language') or 'en'
        lang = str(lang).lower().strip()
        if lang in ['te', 'en']:
            response.set_cookie('rythu_lang', lang, max_age=31536000, path='/', samesite='Lax')

        return response

    # Centralized language-switching API
    @app.route('/api/set-language', methods=['POST', 'GET'])
    def set_language_api():
        if request.method == 'POST':
            data = request.get_json(silent=True) or {}
            lang = data.get('language') or request.form.get('language')
        else:
            lang = request.args.get('lang') or request.args.get('language')

        lang = str(lang or 'te').lower().strip()
        if lang not in ['te', 'en']:
            lang = 'te'

        session['user_language'] = lang

        # If user is authenticated, persist language choice in SQLite database
        user_id = session.get('user_id')
        if user_id:
            try:
                user = User.query.get(user_id)
                if user:
                    user.preferred_language = lang
                    db.session.commit()
            except Exception as e:
                logger.error(f"Error persisting user language to database: {e}")

        resp = make_response(jsonify({'success': True, 'language': lang}))
        resp.set_cookie('rythu_lang', lang, max_age=31536000, path='/', samesite='Lax')
        return resp

    @app.route('/set-language/<lang>')
    def switch_language_redirect(lang):
        lang = str(lang or 'te').lower().strip()
        if lang not in ['te', 'en']:
            lang = 'te'

        session['user_language'] = lang
        user_id = session.get('user_id')
        if user_id:
            try:
                user = User.query.get(user_id)
                if user:
                    user.preferred_language = lang
                    db.session.commit()
            except Exception:
                pass

        next_url = request.args.get('next') or request.referrer or url_for('main.index')
        resp = redirect(next_url)
        resp.set_cookie('rythu_lang', lang, max_age=31536000, path='/', samesite='Lax')
        return resp

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('error.html', error_code=400, error_message=str(error.description)), 400

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error_code=404, error_message="The requested page or endpoint could not be found."), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'success': False,
            'error': 'Uploaded file exceeds the maximum allowed size (16MB).'
        }), 413

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return render_template('error.html', error_code=500, error_message="An internal server error occurred."), 500

    return app


# Create default application instance for WSGI / CLI runners
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "=" * 60)
    print("  🌾 Rythu Mithra (రైతు మిత్ర) Server Starting...")
    print(f"  🌾 Listening on http://localhost:{port}")
    print("=" * 60 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
