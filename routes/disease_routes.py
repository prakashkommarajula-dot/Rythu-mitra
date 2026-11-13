"""
Crop Disease & Pest Detection Routes for Rythu Mithra.
Handles disease prediction UI rendering, image detection UI, and inference API endpoints.
"""

from flask import Blueprint, render_template, request, jsonify, current_app, session
from services.disease_service import analyze_crop_image
from services.nlp_predictor import predict_disease
from services.history_service import save_nlp_prediction
from services.crop_symptoms_service import get_crop_symptoms

disease_bp = Blueprint('disease', __name__)


@disease_bp.route('/predict', methods=['GET'])
def predict_page():
    """Renders the NLP Crop Disease & Pest Prediction interface with voice input."""
    crops = [
        {"id": "Paddy", "name_en": "Paddy (Rice)", "name_te": "వరి"},
        {"id": "Cotton", "name_en": "Cotton", "name_te": "పత్తి"},
        {"id": "Chilli", "name_en": "Chilli", "name_te": "మిరప"},
        {"id": "Tomato", "name_en": "Tomato", "name_te": "టమోటా"},
        {"id": "Bengal Gram", "name_en": "Bengal Gram (Chickpea)", "name_te": "శనగ"},
        {"id": "Groundnut", "name_en": "Groundnut", "name_te": "వేరుశనగ"},
        {"id": "Maize", "name_en": "Maize (Corn)", "name_te": "మొక్కజొన్న"},
        {"id": "Sorghum", "name_en": "Sorghum (Jowar)", "name_te": "జొన్న"},
        {"id": "Turmeric", "name_en": "Turmeric", "name_te": "పసుపు"},
        {"id": "Brinjal", "name_en": "Brinjal (Eggplant)", "name_te": "వంకాయ"},
        {"id": "Other", "name_en": "Other Crops", "name_te": "ఇతర పంటలు"}
    ]
    stages = [
        {"id": "Seedling", "name_en": "Seedling Stage", "name_te": "మొలక దశ"},
        {"id": "Vegetative", "name_en": "Vegetative Stage", "name_te": "శాకీయ దశ"},
        {"id": "Flowering", "name_en": "Flowering Stage", "name_te": "పూత దశ"},
        {"id": "Fruiting", "name_en": "Fruiting / Pod Formation", "name_te": "కాయ / కాయ దశ"},
        {"id": "Harvesting", "name_en": "Maturity / Pre-Harvest", "name_te": "కోత దశ"}
    ]
    return render_template('predict.html', crops=crops, stages=stages)


@disease_bp.route('/image-detection', methods=['GET'])
@disease_bp.route('/disease-detect', methods=['GET'])
def disease_detect_page():
    """Renders the visual crop image disease detection interface."""
    return render_template('image_detection.html')


@disease_bp.route('/api/disease/predict', methods=['POST'])
def predict_disease_api():
    """
    API Endpoint for analyzing crop images.
    Expects multipart/form-data with a 'file' parameter.
    """
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file part in the request. Please upload an image.'
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No image selected. Please choose a crop image to analyze.'
        }), 400

    try:
        # Delegate logic entirely to disease_service
        result = analyze_crop_image(file, current_app.config, user_id=session.get('user_id'))
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error during disease detection API call: {e}")
        return jsonify({
            'success': False,
            'error': f"Internal server error processing image: {str(e)}"
        }), 500


@disease_bp.route('/api/crop-symptoms', methods=['GET'])
def crop_symptoms_api():
    """
    Returns dataset-derived symptom chips and diagnostic questions for a selected crop.
    Query parameters:
    - crop: Target crop name (e.g. Groundnut, Paddy, Cotton, Chilli)
    - lang: Preferred language ('te' or 'en')
    """
    crop = request.args.get('crop') or request.args.get('crop_name')
    lang = request.args.get('lang') or request.cookies.get('rythu_lang') or session.get('user_language') or 'en'
    result = get_crop_symptoms(crop, lang=lang)
    return jsonify(result), 200


@disease_bp.route('/api/predict', methods=['POST'])
def predict_nlp_api():
    """
    NLP Disease & Pest Prediction Endpoint for text symptom descriptions.
    Expects JSON body:
    {
        "description": "టమాట కాయల మీద రంధ్రం చేసి పురుగు లోపలికి వెళ్ళినట్టు ఉంది",
        "crop": "Tomato",
        "crop_stage": "Fruiting",
        "season": "Kharif",
        "language": "te",
        "answers": ["Leaves have circular brown spots", "No webbing"] (optional)
    }
    """
    data = request.get_json(silent=True) or {}
    description = (data.get('description') or data.get('text') or '').strip()
    crop_name = data.get('crop') or data.get('crop_name') or ''
    crop_stage = data.get('crop_stage') or 'Not specified'
    season = data.get('season') or 'Kharif'
    language = data.get('language') or request.cookies.get('rythu_lang') or session.get('user_language') or 'en'
    answers = data.get('answers')

    if answers:
        if isinstance(answers, list):
            ans_str = " | Details: " + " ; ".join(str(a) for a in answers if a)
        elif isinstance(answers, dict):
            ans_str = " | Details: " + " ; ".join(f"{k}: {v}" for k, v in answers.items() if v)
        else:
            ans_str = f" | Details: {answers}"
        description = f"{description}{ans_str}"

    if not description:
        return jsonify({
            'success': False,
            'prediction': 'Unknown',
            'score': 0.0,
            'top_predictions': [],
            'needs_further_diagnosis': True,
            'message': 'Description field is required and cannot be empty.'
        }), 400

    try:
        result = predict_disease(
            text=description,
            crop=crop_name,
            crop_stage=crop_stage,
            season=season,
            language=language
        )
        status_code = 200 if result.get('success', False) else 400

        # Save to database for dashboard history if prediction succeeded
        if result.get('success', False):
            final_crop = crop_name or result.get('crop') or 'General'
            user_id = session.get('user_id')
            pred_id = save_nlp_prediction(
                crop_name=final_crop,
                crop_stage=crop_stage,
                symptom_description=description,
                result=result,
                language=language or 'en',
                user_id=user_id
            )
            result['prediction_id'] = pred_id
            result['crop'] = final_crop
            result['symptom_description'] = description
            req_lang = language or 'en'
            if result.get('needs_further_diagnosis'):
                result['advisory_url'] = f"/advisory?needs_further_diagnosis=true&crop={final_crop}&prediction_id={pred_id}&lang={req_lang}"
            else:
                result['advisory_url'] = f"/advisory?disease={result['prediction']}&crop={final_crop}&score={result.get('score', 0)}&prediction_id={pred_id}&lang={req_lang}"

        return jsonify(result), status_code
    except Exception as e:
        current_app.logger.error(f"Error during NLP predict endpoint: {e}")
        return jsonify({
            'success': False,
            'prediction': 'Error',
            'score': 0.0,
            'top_predictions': [],
            'needs_further_diagnosis': True,
            'message': f"Internal server error during prediction: {str(e)}"
        }), 500

