import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration with shared application parameters."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'rythu-mithra-final-year-insecure-secret-key-change-in-prod')
    DEBUG = False
    TESTING = False

    # Database Configuration (SQLite)
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'rythu_mithra.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session & Cookie Security (Phase 5)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Set to True when HTTPS is enabled in production
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 Days session duration

    # Uploads Configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    # Machine Learning Models Configuration
    # Models are stored in models/checkpoints/
    CROP_DISEASE_MODEL_PATH = os.environ.get(
        'CROP_DISEASE_MODEL_PATH',
        os.path.join(BASE_DIR, 'models', 'checkpoints', 'crop_disease_model.keras')
    )
    XLM_ROBERTA_MODEL_DIR = os.environ.get(
        'XLM_ROBERTA_MODEL_DIR',
        os.path.join(BASE_DIR, 'models', 'checkpoints', 'xlm_roberta')
    )
    DISEASE_METADATA_PATH = os.path.join(BASE_DIR, 'models', 'disease_metadata.json')

    # Image Preprocessing Settings
    IMAGE_TARGET_SIZE = (224, 224)

    # Supported Languages for Multilingual Advisory and Voice Input
    SUPPORTED_LANGUAGES = {
        'te': {'name': 'Telugu', 'native': 'తెలుగు', 'speech_code': 'te-IN'},
        'hi': {'name': 'Hindi', 'native': 'हिन्दी', 'speech_code': 'hi-IN'},
        'en': {'name': 'English', 'native': 'English', 'speech_code': 'en-IN'},
        'ta': {'name': 'Tamil', 'native': 'தமிழ்', 'speech_code': 'ta-IN'},
        'kn': {'name': 'Kannada', 'native': 'ಕನ್ನಡ', 'speech_code': 'kn-IN'}
    }
    DEFAULT_LANGUAGE = 'te'


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration with stricter settings."""
    DEBUG = False
    # Ensure SECRET_KEY is set in production
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'tests', 'test_uploads')


# Dictionary mapping environment names to configuration classes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
