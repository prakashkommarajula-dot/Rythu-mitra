"""
Routes package for Rythu Mithra.
Contains modular blueprints separating web page rendering and API endpoints.
"""

from .main_routes import main_bp
from .disease_routes import disease_bp
from .advisory_routes import advisory_bp

__all__ = ['main_bp', 'disease_bp', 'advisory_bp']
