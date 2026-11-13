"""
History and Analytics Service for Rythu Mithra.
Phase 5: Secure Prediction Audit, Strict Farmer Data Isolation, and Advanced Filtering.
"""

from datetime import datetime, time
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy import or_, and_
from database import db
from database.models import DiseaseDetectionRecord, AdvisoryQueryRecord, NLPPredictionRecord, User

logger = logging.getLogger(__name__)


def save_nlp_prediction(
    crop_name: str,
    crop_stage: str,
    symptom_description: str,
    result: Dict[str, Any],
    language: str = 'te',
    user_id: Optional[int] = None
) -> Optional[int]:
    """
    Saves an NLP prediction result to SQLite database linked to the logged-in farmer.
    Returns the newly created record ID or None if saving failed.
    """
    try:
        rec = NLPPredictionRecord(
            user_id=user_id,
            crop_name=crop_name or 'General',
            crop_stage=crop_stage or 'Not specified',
            symptom_description=symptom_description,
            detected_disease=result.get('prediction', 'Unknown'),
            confidence_score=float(result.get('score', 0.0)),
            top_predictions=result.get('top_predictions', []),
            needs_further_diagnosis=bool(result.get('needs_further_diagnosis', False)),
            language=language or 'te',
            created_at=datetime.utcnow()
        )
        db.session.add(rec)
        db.session.commit()
        logger.info(f"Saved NLPPredictionRecord #{rec.id} for user_id={user_id} ({rec.detected_disease})")
        return rec.id
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving NLP prediction: {e}")
        return None


def get_recent_nlp_predictions(
    user_id: Optional[int] = None,
    limit: int = 50,
    crop: Optional[str] = None,
    disease: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetches NLP prediction records with strict farmer data isolation and parameterized filtering.
    If user_id is provided, only records belonging to that farmer are returned.
    """
    try:
        query = NLPPredictionRecord.query

        # Enforce farmer data isolation
        if user_id is not None:
            query = query.filter(NLPPredictionRecord.user_id == user_id)

        # Filter by Crop
        if crop and crop.strip() and crop.lower() != 'all':
            query = query.filter(NLPPredictionRecord.crop_name.ilike(f"%{crop.strip()}%"))

        # Filter by Disease / Pest
        if disease and disease.strip() and disease.lower() != 'all':
            query = query.filter(NLPPredictionRecord.detected_disease.ilike(f"%{disease.strip()}%"))

        # Filter by Search Keyword (symptoms or disease name)
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    NLPPredictionRecord.symptom_description.ilike(term),
                    NLPPredictionRecord.detected_disease.ilike(term),
                    NLPPredictionRecord.crop_name.ilike(term)
                )
            )

        # Filter by Date Range
        if date_from and date_from.strip():
            try:
                dt_from = datetime.strptime(date_from.strip(), '%Y-%m-%d')
                query = query.filter(NLPPredictionRecord.created_at >= dt_from)
            except ValueError:
                pass

        if date_to and date_to.strip():
            try:
                dt_to = datetime.strptime(date_to.strip(), '%Y-%m-%d')
                dt_to_end = datetime.combine(dt_to.date(), time.max)
                query = query.filter(NLPPredictionRecord.created_at <= dt_to_end)
            except ValueError:
                pass

        records = query.order_by(NLPPredictionRecord.created_at.desc()).limit(limit).all()
        return [r.to_dict() for r in records]
    except Exception as e:
        logger.error(f"Error querying NLP predictions: {e}")
        return []


def get_prediction_by_id(prediction_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches a specific prediction record, preventing Insecure Direct Object Reference (IDOR)
    by verifying that the record belongs to the requesting user_id.
    """
    try:
        query = NLPPredictionRecord.query.filter_by(id=prediction_id)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        rec = query.first()
        return rec.to_dict() if rec else None
    except Exception as e:
        logger.error(f"Error retrieving prediction #{prediction_id}: {e}")
        return None


def get_recent_detections(user_id: Optional[int] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch recent crop disease detection records (image-based) with farmer isolation."""
    try:
        query = DiseaseDetectionRecord.query
        if user_id is not None:
            query = query.filter(DiseaseDetectionRecord.user_id == user_id)
        records = query.order_by(DiseaseDetectionRecord.created_at.desc()).limit(limit).all()
        return [r.to_dict() for r in records]
    except Exception as e:
        logger.error(f"Error querying image detections: {e}")
        return []


def get_recent_advisories(user_id: Optional[int] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch recent advisory queries and responses with farmer isolation."""
    try:
        query = AdvisoryQueryRecord.query
        if user_id is not None:
            query = query.filter(AdvisoryQueryRecord.user_id == user_id)
        records = query.order_by(AdvisoryQueryRecord.created_at.desc()).limit(limit).all()
        return [r.to_dict() for r in records]
    except Exception as e:
        logger.error(f"Error querying advisories: {e}")
        return []


def get_dashboard_summary(user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Returns authentic summary counts for the dashboard from real database records.
    When user_id is provided, aggregates counts specifically for that logged-in farmer.
    """
    try:
        if user_id is not None:
            # Farmer-specific counts
            image_detections = DiseaseDetectionRecord.query.filter_by(user_id=user_id).count()
            nlp_predictions = NLPPredictionRecord.query.filter_by(user_id=user_id).count()
            total_predictions = image_detections + nlp_predictions
            total_advisories = AdvisoryQueryRecord.query.filter_by(user_id=user_id).count()
            voice_queries = AdvisoryQueryRecord.query.filter_by(user_id=user_id, input_type='voice').count()
            text_queries = AdvisoryQueryRecord.query.filter_by(user_id=user_id, input_type='text').count()
            total_users = 1
        else:
            # Global platform counts
            image_detections = DiseaseDetectionRecord.query.count()
            nlp_predictions = NLPPredictionRecord.query.count()
            total_predictions = image_detections + nlp_predictions
            total_advisories = AdvisoryQueryRecord.query.count()
            voice_queries = AdvisoryQueryRecord.query.filter_by(input_type='voice').count()
            text_queries = AdvisoryQueryRecord.query.filter_by(input_type='text').count()
            total_users = User.query.count()
    except Exception as e:
        logger.error(f"Error aggregating dashboard summary: {e}")
        image_detections = 0
        nlp_predictions = 0
        total_predictions = 0
        total_advisories = 0
        voice_queries = 0
        text_queries = 0
        total_users = 0

    return {
        'total_predictions': total_predictions,
        'image_detections': image_detections,
        'nlp_predictions': nlp_predictions,
        'total_advisories': total_advisories,
        'voice_queries': voice_queries,
        'text_queries': text_queries,
        'total_users': total_users
    }
