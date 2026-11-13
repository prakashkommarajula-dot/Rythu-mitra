"""
Rythu Mithra - Database Migration for Phase 6
Safely adds 'advisory_views' table to existing SQLite database without deleting or resetting any tables.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'database' / 'rythu_mithra.db'


def migrate():
    print(f"[*] Checking database schema for Phase 6 at: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Create advisory_views table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS advisory_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        prediction_id INTEGER REFERENCES nlp_predictions(id),
        disease_or_pest VARCHAR(150) NOT NULL,
        crop VARCHAR(100),
        language VARCHAR(10) DEFAULT 'te',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create indexes for fast lookup and farmer isolation
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_advisory_views_user ON advisory_views(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_advisory_views_pred ON advisory_views(prediction_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_advisory_views_disease ON advisory_views(disease_or_pest);")

    conn.commit()
    conn.close()
    print("[SUCCESS] Phase 6 database migration completed successfully!")


if __name__ == '__main__':
    migrate()
