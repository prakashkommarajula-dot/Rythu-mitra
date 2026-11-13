"""
Disease Detection Service for Rythu Mithra.
Coordinates image processing, TensorFlow model inference, metadata retrieval,
and database persistence.
"""

import os
import logging
from database import db
from database.models import DiseaseDetectionRecord
from models.model_loader import CropDiseaseModelLoader, ModelNotReadyError
from utils.file_handler import save_uploaded_image

logger = logging.getLogger(__name__)


def analyze_crop_image(file_storage, app_config, user_id=None):
    """
    Analyzes an uploaded crop image file.
    
    Args:
        file_storage: Werkzeug FileStorage object from request.files
        app_config: Flask app config object or dict
        
    Returns:
        dict: Analysis result containing prediction details or model status instructions.
    """
    upload_folder = app_config.get('UPLOAD_FOLDER')
    allowed_extensions = app_config.get('ALLOWED_EXTENSIONS')
    model_path = app_config.get('CROP_DISEASE_MODEL_PATH')
    metadata_path = app_config.get('DISEASE_METADATA_PATH')
    target_size = app_config.get('IMAGE_TARGET_SIZE', (224, 224))

    # 1. Validate and save image to uploads directory
    filename, file_path = save_uploaded_image(file_storage, upload_folder, allowed_extensions)
    image_url = f"/static/uploads/{filename}"

    # 2. Initialize or get model loader singleton
    loader = CropDiseaseModelLoader(
        model_path=model_path,
        metadata_path=metadata_path,
        target_size=target_size
    )

    # 3. Check if real model weights are mounted
    if not loader.is_loaded:
        logger.info("Model weights not mounted yet. Returning uploaded image with setup instructions.")
        return {
            'success': True,
            'model_ready': False,
            'message': (
                "Image uploaded successfully. To enable live AI disease detection, "
                "place your trained TensorFlow/Keras model (.keras or .h5) in 'models/checkpoints/' "
                "as described in models/checkpoints/README.md."
            ),
            'filename': filename,
            'image_url': image_url,
            'available_classes': loader.classes,
            'model_status': {
                'loaded': False,
                'expected_path': model_path,
                'error': loader.load_error
            }
        }

    # 4. Preprocess image
    try:
        tensor = loader.preprocess_image(file_path)
    except Exception as e:
        logger.error(f"Image preprocessing failed for {filename}: {e}")
        return {
            'success': False,
            'model_ready': True,
            'error': f"Image processing failed: {str(e)}",
            'image_url': image_url
        }

    # 5. Run real TensorFlow inference
    try:
        predicted_class, confidence, all_probs = loader.predict(tensor)
    except ModelNotReadyError as e:
        return {
            'success': False,
            'model_ready': False,
            'error': str(e),
            'image_url': image_url
        }
    except Exception as e:
        logger.error(f"Inference execution failed: {e}")
        return {
            'success': False,
            'model_ready': True,
            'error': f"Model prediction error: {str(e)}",
            'image_url': image_url
        }

    # 6. Retrieve disease remediation metadata
    disease_info = loader.metadata.get(predicted_class, {
        'crop': 'Crop',
        'disease': predicted_class.replace('_', ' '),
        'telugu_name': predicted_class,
        'hindi_name': predicted_class,
        'symptoms': {'en': 'Information pending for this disease class.'},
        'organic_remedies': {'en': 'Follow integrated pest management protocols.'},
        'chemical_treatment': {'en': 'Consult local Krishi Vigyan Kendra (KVK).'},
        'severity': 'Moderate'
    })

    # 7. Persist diagnosis record to SQLite database
    record = DiseaseDetectionRecord(
        user_id=user_id,
        filename=filename,
        image_path=file_path,
        detected_crop=disease_info.get('crop', 'Crop'),
        detected_disease=disease_info.get('disease', predicted_class),
        confidence=confidence,
        severity=disease_info.get('severity', 'Moderate'),
        recommendations=disease_info
    )
    db.session.add(record)
    db.session.commit()

    return {
        'success': True,
        'model_ready': True,
        'record_id': record.id,
        'filename': filename,
        'image_url': image_url,
        'predicted_class': predicted_class,
        'crop': disease_info.get('crop'),
        'disease': disease_info.get('disease'),
        'telugu_name': disease_info.get('telugu_name'),
        'hindi_name': disease_info.get('hindi_name'),
        'confidence': round(confidence * 100, 2),
        'severity': disease_info.get('severity'),
        'symptoms': disease_info.get('symptoms'),
        'organic_remedies': disease_info.get('organic_remedies'),
        'chemical_treatment': disease_info.get('chemical_treatment'),
        'all_probabilities': all_probs
    }
