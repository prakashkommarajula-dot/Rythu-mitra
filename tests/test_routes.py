"""
Automated Route & API Integration Tests for Rythu Mithra.
"""

import pytest
import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from database import db


@pytest.fixture
def client():
    """Create and configure a Flask test client using TestingConfig."""
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_index_route(client):
    """Test dashboard landing page renders successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Rythu Mithra" in response.data


def test_disease_detect_page(client):
    """Test disease detection page renders successfully."""
    response = client.get('/disease-detect')
    assert response.status_code == 200
    assert b"Visual Leaf Disease" in response.data or b"Disease" in response.data


def test_advisory_page(client):
    """Test multilingual advisory page renders successfully."""
    response = client.get('/advisory')
    assert response.status_code == 200
    assert b"Agricultural Advisory" in response.data


def test_history_page(client):
    """Test history page redirects to login when unauthenticated."""
    response = client.get('/history')
    assert response.status_code in [200, 302]


def test_about_page(client):
    """Test about page renders successfully."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b"System Architecture" in response.data or b"Architecture" in response.data


def test_advisory_samples_api(client):
    """Test sample queries endpoint returns list."""
    response = client.get('/api/advisory/samples')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert isinstance(data['samples'], list)


def test_advisory_query_api_telugu(client):
    """Test advisory API with Telugu query."""
    payload = {
        'query': 'వరి పంటలో అగ్గి తెగులు నివారణ ఏమిటి?',
        'language': 'te',
        'input_type': 'text'
    }
    response = client.post('/api/advisory/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'ట్రైసైక్లాజోల్' in data['response'] or 'సూడోమోనాస్' in data['response']


def test_advisory_query_api_empty_query(client):
    """Test advisory API returns 400 when query is empty."""
    response = client.post('/api/advisory/query', json={'query': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_disease_predict_missing_file(client):
    """Test disease predict endpoint returns 400 when no file is uploaded."""
    response = client.post('/api/disease/predict')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
