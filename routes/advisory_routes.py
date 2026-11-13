"""
Multilingual Agricultural Advisory Routes for Rythu Mithra.
Phase 6: Smart Integrated Pest Management (IPM), Follow-Up Diagnosis, and Verified Advice.
"""

import os
import json
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

from flask import Blueprint, render_template, request, jsonify, current_app, session
from services.advisory_service import (
    get_advisory,
    get_fallback_advisory,
    log_advisory_view,
    advisory_engine,
    process_advisory_query
)
from services.nlp_predictor import predict_disease
from services.history_service import save_nlp_prediction

logger = logging.getLogger(__name__)
advisory_bp = Blueprint('advisory', __name__)


@advisory_bp.route('/advisory', methods=['GET'])
def advisory_page():
    """
    Renders the Smart Agricultural Advisory interface.
    Supports:
    - Direct access for searching / asking questions.
    - Deep-linking from NLP Prediction workspace with predicted disease & crop.
    - Diagnostic fallback for uncertain predictions requiring further field inspection.
    """
    languages = current_app.config.get('SUPPORTED_LANGUAGES', {})
    
    # Query parameters from prediction or navigation
    disease_param = request.args.get('disease', '').strip()
    crop_param = request.args.get('crop', '').strip()
    prediction_id = request.args.get('prediction_id', type=int)
    score = request.args.get('score', type=float)
    needs_further = request.args.get('needs_further_diagnosis', '').lower() in ['true', '1', 'yes']
    lang = request.args.get('lang') or request.cookies.get('rythu_lang') or session.get('user_language') or 'te'
    lang = str(lang).lower().strip()
    if lang not in ['te', 'en']:
        lang = 'te'

    advisory_data = None
    not_found_message = None

    if needs_further or (disease_param and 'further diagnosis' in disease_param.lower()):
        # Retrieve fallback diagnostic questions and safe cultural advice
        advisory_data = get_fallback_advisory(crop=crop_param, language=lang)
    elif disease_param:
        advisory_data = get_advisory(
            disease_or_pest=disease_param,
            crop=crop_param,
            language=lang
        )
        if advisory_data:
            # Audit log view for authenticated farmer
            user_id = session.get('user_id')
            if user_id:
                log_advisory_view(
                    user_id=user_id,
                    disease_or_pest=disease_param,
                    crop=crop_param,
                    prediction_id=prediction_id,
                    language=lang
                )
        else:
            not_found_message = f"No verified agricultural advisory entry found for '{disease_param}'."

    available_diseases = advisory_engine.get_available_diseases()

    return render_template(
        'advisory.html',
        languages=languages,
        advisory=advisory_data,
        disease_param=disease_param,
        crop_param=crop_param,
        score=score,
        prediction_id=prediction_id,
        needs_further=needs_further,
        selected_lang=lang,
        not_found_message=not_found_message,
        available_diseases=available_diseases
    )


@advisory_bp.route('/api/advisory/retrieve', methods=['POST'])
def retrieve_advisory_api():
    """
    API endpoint to retrieve verified 9-section advisory JSON by disease and crop.
    Expects JSON:
    {
        "disease": "Blast",
        "crop": "Rice",
        "language": "te"
    }
    """
    data = request.get_json(silent=True) or {}
    disease = data.get('disease', '').strip()
    crop = data.get('crop', '').strip()
    language = data.get('language', 'te').strip().lower()

    if not disease:
        return jsonify({'success': False, 'error': 'Disease parameter is required.'}), 400

    if 'further diagnosis' in disease.lower():
        advisory = get_fallback_advisory(crop=crop, language=language)
        return jsonify({'success': True, 'advisory': advisory}), 200

    advisory = get_advisory(disease_or_pest=disease, crop=crop, language=language)
    if not advisory:
        return jsonify({
            'success': False,
            'error': f"No verified advisory found for '{disease}'."
        }), 404

    # Log view if user is logged in
    user_id = session.get('user_id')
    if user_id:
        log_advisory_view(
            user_id=user_id,
            disease_or_pest=disease,
            crop=crop,
            language=language
        )

    return jsonify({'success': True, 'advisory': advisory}), 200


@advisory_bp.route('/api/predict/follow-up', methods=['POST'])
def predict_follow_up_api():
    """
    Multi-turn follow-up diagnosis endpoint.
    When a diagnosis requires further observation, this receives the farmer's answers
    to diagnostic questions, combines them with initial context, and re-predicts.
    Expects JSON:
    {
        "original_description": "ఆకులు పసుపుగా మారాయి",
        "follow_up": "ఆకులపై కండె ఆకారపు మచ్చలు కనిపించాయి మరియు గడ్డిలా ఎండిపోతున్నాయి",
        "crop": "Rice",
        "language": "te",
        "prediction_id": 12 (optional)
    }
    """
    data = request.get_json(silent=True) or {}
    original = data.get('original_description', '').strip()
    follow_up = data.get('follow_up', '').strip()
    crop = data.get('crop', 'General').strip()
    language = data.get('language', 'te').strip().lower()

    if not follow_up:
        return jsonify({
            'success': False,
            'error': 'Please provide answers or additional symptom observations.'
        }), 400

    # Combine original observations with follow-up field answers
    combined_query = f"{original} {follow_up}".strip()

    try:
        result = predict_disease(text=combined_query, language=language)
        
        # If prediction succeeded and is now confident
        is_confident = result.get('success', False) and not result.get('needs_further_diagnosis', False)
        user_id = session.get('user_id')

        if result.get('success', False):
            # Save updated prediction in audit history
            new_pred_id = save_nlp_prediction(
                crop_name=crop,
                crop_stage="Follow-up Re-diagnosis",
                symptom_description=combined_query,
                result=result,
                language=language,
                user_id=user_id
            )
            result['prediction_id'] = new_pred_id

        # Attach direct advisory URL
        if is_confident:
            result['advisory_url'] = f"/advisory?disease={result['prediction']}&crop={crop}&score={result['score']}&prediction_id={result.get('prediction_id')}"
        else:
            result['advisory_url'] = f"/advisory?needs_further_diagnosis=true&crop={crop}"

        return jsonify({
            'success': True,
            'is_confident': is_confident,
            'result': result
        }), 200
    except Exception as e:
        logger.error(f"Error during follow-up diagnosis: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@advisory_bp.route('/api/advisory/query', methods=['POST'])
def query_advisory_api():
    """
    Legacy API endpoint for multilingual agricultural advisory queries.
    Accepts JSON body:
    {
        "query": "వరిలో అగ్గి తెగులు నివారణ ఏమిటి?",
        "language": "te",
        "input_type": "voice" | "text"
    }
    """
    data = request.get_json(silent=True) or {}
    query_text = data.get('query', '').strip()
    language = data.get('language', current_app.config.get('DEFAULT_LANGUAGE', 'te'))
    input_type = data.get('input_type', 'text')

    if not query_text:
        return jsonify({
            'success': False,
            'error': 'Query text is required.'
        }), 400

    try:
        result = process_advisory_query(
            query_text=query_text,
            language=language,
            input_type=input_type,
            app_config=current_app.config,
            user_id=session.get('user_id')
        )
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Error during advisory query processing: {e}")
        return jsonify({
            'success': False,
            'error': f"Failed to generate agricultural advisory: {str(e)}"
        }), 500


@advisory_bp.route('/api/advisory/samples', methods=['GET'])
def get_sample_queries_api():
    """Returns sample queries from data/sample_queries.json."""
    samples_path = os.path.join(current_app.config.get('BASE_DIR', str(PROJECT_ROOT)), 'data', 'sample_queries.json')
    if os.path.exists(samples_path):
        try:
            with open(samples_path, 'r', encoding='utf-8') as f:
                samples = json.load(f)
            return jsonify({'success': True, 'samples': samples}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    return jsonify({'success': True, 'samples': []}), 200
