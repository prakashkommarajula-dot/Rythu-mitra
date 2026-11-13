"""
Unit tests for Rythu Mithra Services and Utilities.
"""

import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from database import db
from utils.file_handler import allowed_file
from services.advisory_service import process_advisory_query
from models.model_loader import CropDiseaseModelLoader, XlmRobertaAdvisoryLoader


@pytest.fixture
def app_ctx():
    """Create Flask application context for testing."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app


def test_allowed_file():
    """Verify allowed image extensions checker."""
    allowed = {'png', 'jpg', 'jpeg', 'webp'}
    assert allowed_file('leaf.jpg', allowed) is True
    assert allowed_file('crop.PNG', allowed) is True
    assert allowed_file('dataset.csv', allowed) is False
    assert allowed_file('script.py', allowed) is False
    assert allowed_file('noextension', allowed) is False


def test_advisory_service_telugu(app_ctx):
    """Verify multilingual advisory service responses in Telugu."""
    res = process_advisory_query(
        query_text='ప్రత్తి పంటలో తెల్లదోమ నివారణ',
        language='te',
        input_type='voice',
        app_config=app_ctx.config
    )
    assert res['success'] is True
    assert res['language'] == 'te'
    assert 'జిగురు అట్టలను' in res['response'] or 'వేప నూనెను' in res['response']
    assert res['input_type'] == 'voice'


def test_advisory_service_hindi(app_ctx):
    """Verify multilingual advisory service responses in Hindi."""
    res = process_advisory_query(
        query_text='धान में ब्लास्ट रोग का नियंत्रण कैसे करें',
        language='hi',
        input_type='text',
        app_config=app_ctx.config
    )
    assert res['success'] is True
    assert res['language'] == 'hi'
    assert 'झुलसा' in res['response'] or 'ट्राइसाइक्लाजोल' in res['response']


def test_crop_disease_model_loader_missing_weights():
    """Ensure CropDiseaseModelLoader handles absent weights gracefully without unhandled exceptions."""
    loader = CropDiseaseModelLoader(
        model_path='models/checkpoints/non_existent_weights.keras',
        metadata_path='models/disease_metadata.json'
    )
    assert loader.is_loaded is False
    assert loader.load_error is not None
    assert len(loader.classes) > 0


def test_xlm_roberta_loader_missing_checkpoint():
    """Ensure XlmRobertaAdvisoryLoader handles absent checkpoint gracefully."""
    loader = XlmRobertaAdvisoryLoader(
        model_dir='models/checkpoints/non_existent_roberta'
    )
    assert loader.is_loaded is False
    assert loader.load_error is not None
