"""
SQLAlchemy models for Rythu Mithra application.
Phase 5: Farmer Profile Authentication, Prediction Audit & Isolation, and History.
"""

from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    """
    Stores farmer account profiles for Rythu Mithra.
    Supports secure authentication, location details, and language preference.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    mobile_number = db.Column(db.String(20), unique=True, nullable=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    phone_or_email = db.Column(db.String(120), nullable=True)  # Backward compatibility
    password_hash = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(100), default='Andhra Pradesh')
    district = db.Column(db.String(100), nullable=False, default='Guntur')
    mandal = db.Column(db.String(100), nullable=True)
    preferred_language = db.Column(db.String(10), default='te')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    nlp_predictions = db.relationship(
        'NLPPredictionRecord',
        backref=db.backref('farmer', lazy=True),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    disease_detections = db.relationship(
        'DiseaseDetectionRecord',
        backref=db.backref('farmer', lazy=True),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    advisory_queries = db.relationship(
        'AdvisoryQueryRecord',
        backref=db.backref('farmer', lazy=True),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    advisory_views = db.relationship(
        'AdvisoryViewRecord',
        backref=db.backref('farmer', lazy=True),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def set_password(self, password: str):
        """Hashes password using secure Werkzeug pbkdf2/scrypt utilities."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies candidate plaintext password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serializes user record to dictionary (excluding password_hash)."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'mobile_number': self.mobile_number,
            'email': self.email,
            'phone_or_email': self.phone_or_email or self.mobile_number or self.email,
            'state': self.state,
            'district': self.district,
            'mandal': self.mandal or 'Not specified',
            'preferred_language': self.preferred_language,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<User {self.id}: {self.full_name} ({self.mobile_number})>'


class DiseaseDetectionRecord(db.Model):
    """Stores records of crop images analyzed for disease and pest detection."""
    __tablename__ = 'disease_detections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    filename = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    detected_crop = db.Column(db.String(100), nullable=False)
    detected_disease = db.Column(db.String(150), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(50), default='Moderate')
    recommendations_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def recommendations(self):
        """Parse recommendations JSON string to Python dictionary."""
        if self.recommendations_json:
            try:
                return json.loads(self.recommendations_json)
            except (ValueError, TypeError):
                return {}
        return {}

    @recommendations.setter
    def recommendations(self, value):
        """Serialize recommendations dictionary to JSON string."""
        if isinstance(value, (dict, list)):
            self.recommendations_json = json.dumps(value)
        elif isinstance(value, str):
            self.recommendations_json = value
        else:
            self.recommendations_json = "{}"

    def to_dict(self):
        """Serialize model to dictionary for API responses."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'image_url': f'/static/uploads/{self.filename}',
            'detected_crop': self.detected_crop,
            'detected_disease': self.detected_disease,
            'confidence': round(self.confidence * 100, 2) if self.confidence <= 1.0 else round(self.confidence, 2),
            'severity': self.severity,
            'recommendations': self.recommendations,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<DiseaseDetectionRecord {self.id}: {self.detected_crop} - {self.detected_disease}>'


class AdvisoryQueryRecord(db.Model):
    """Stores multilingual user queries and generated agricultural advisories."""
    __tablename__ = 'advisory_queries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    user_query = db.Column(db.Text, nullable=False)
    detected_language = db.Column(db.String(10), default='te')
    input_type = db.Column(db.String(20), default='text')  # 'voice' or 'text'
    response_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='General Advisory')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Serialize model to dictionary for API responses."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_query': self.user_query,
            'detected_language': self.detected_language,
            'input_type': self.input_type,
            'response_text': self.response_text,
            'category': self.category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<AdvisoryQueryRecord {self.id}: [{self.detected_language}] {self.user_query[:30]}>'


class NLPPredictionRecord(db.Model):
    """
    Stores NLP-based crop disease & pest predictions submitted by farmers.
    Maintains farmer association, symptom text, top-3 candidates, and uncertainty status.
    """
    __tablename__ = 'nlp_predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    crop_name = db.Column(db.String(100), default='General')
    crop_stage = db.Column(db.String(50), nullable=True)
    symptom_description = db.Column(db.Text, nullable=False)
    detected_disease = db.Column(db.String(150), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    top_predictions_json = db.Column(db.Text, nullable=True)
    needs_further_diagnosis = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(10), default='te')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def top_predictions(self):
        if self.top_predictions_json:
            try:
                return json.loads(self.top_predictions_json)
            except (ValueError, TypeError):
                return []
        return []

    @top_predictions.setter
    def top_predictions(self, value):
        if isinstance(value, (dict, list)):
            self.top_predictions_json = json.dumps(value)
        elif isinstance(value, str):
            self.top_predictions_json = value
        else:
            self.top_predictions_json = "[]"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crop_name': self.crop_name,
            'crop_stage': self.crop_stage or 'Not specified',
            'symptom_description': self.symptom_description,
            'detected_disease': self.detected_disease,
            'confidence_score': round(self.confidence_score * 100, 2) if self.confidence_score <= 1.0 else round(self.confidence_score, 2),
            'top_predictions': self.top_predictions,
            'needs_further_diagnosis': self.needs_further_diagnosis,
            'language': self.language,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<NLPPredictionRecord {self.id}: {self.crop_name} - {self.detected_disease}>'


class AdvisoryViewRecord(db.Model):
    """
    Stores audit logs of agricultural advisories reviewed by authenticated farmers.
    Links viewed disease/pest remedy guidelines to prediction records and farmer profiles.
    """
    __tablename__ = 'advisory_views'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('nlp_predictions.id'), nullable=True, index=True)
    disease_or_pest = db.Column(db.String(150), nullable=False)
    crop = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), default='te')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'prediction_id': self.prediction_id,
            'disease_or_pest': self.disease_or_pest,
            'crop': self.crop,
            'language': self.language,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<AdvisoryViewRecord {self.id}: {self.disease_or_pest} (User: {self.user_id})>'

