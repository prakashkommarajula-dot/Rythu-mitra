"""
Database Initialization Script for Rythu Mithra.
Run this script directly to create SQLite database tables:
    python database/init_db.py
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from flask import Flask
from config import Config
from database import db, init_db
from database.models import DiseaseDetectionRecord, AdvisoryQueryRecord


def create_initial_database():
    """Create all SQLite database tables using the Flask application context."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database directory exists
    db_dir = Path(app.config['DATABASE_PATH']).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Ensure upload directory exists
    upload_dir = Path(app.config['UPLOAD_FOLDER'])
    upload_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Initializing database at: {app.config['DATABASE_PATH']}")
    init_db(app)

    with app.app_context():
        # Verify tables are created
        tables = db.metadata.tables.keys()
        print("[+] Database tables initialized successfully:")
        for table in tables:
            print(f"    - {table}")


if __name__ == '__main__':
    create_initial_database()
