"""
Rythu Mithra - Database Migration for Phase 5
Safely adds Phase 5 columns to existing SQLite database without deleting or resetting any tables.
"""

import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'database' / 'rythu_mithra.db'


def migrate():
    print(f"[*] Checking database schema at: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Helper function to check if column exists
    def column_exists(table, column):
        cursor.execute(f"PRAGMA table_info({table});")
        cols = [info[1] for info in cursor.fetchall()]
        return column in cols

    # 1. Update 'users' table
    user_columns = [
        ("mobile_number", "VARCHAR(20)"),
        ("email", "VARCHAR(120)"),
        ("state", "VARCHAR(100) DEFAULT 'Andhra Pradesh'"),
        ("mandal", "VARCHAR(100)"),
    ]
    for col_name, col_type in user_columns:
        if not column_exists("users", col_name):
            print(f"[+] Adding column '{col_name}' to 'users' table...")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
        else:
            print(f"[-] Column '{col_name}' already exists in 'users'.")

    # 2. Update 'nlp_predictions' table
    nlp_columns = [
        ("user_id", "INTEGER REFERENCES users(id)"),
    ]
    for col_name, col_type in nlp_columns:
        if not column_exists("nlp_predictions", col_name):
            print(f"[+] Adding column '{col_name}' to 'nlp_predictions' table...")
            cursor.execute(f"ALTER TABLE nlp_predictions ADD COLUMN {col_name} {col_type};")
        else:
            print(f"[-] Column '{col_name}' already exists in 'nlp_predictions'.")

    # 3. Update 'disease_detections' table
    disease_columns = [
        ("user_id", "INTEGER REFERENCES users(id)"),
    ]
    for col_name, col_type in disease_columns:
        if not column_exists("disease_detections", col_name):
            print(f"[+] Adding column '{col_name}' to 'disease_detections' table...")
            cursor.execute(f"ALTER TABLE disease_detections ADD COLUMN {col_name} {col_type};")
        else:
            print(f"[-] Column '{col_name}' already exists in 'disease_detections'.")

    # 4. Update 'advisory_queries' table
    advisory_columns = [
        ("user_id", "INTEGER REFERENCES users(id)"),
    ]
    for col_name, col_type in advisory_columns:
        if not column_exists("advisory_queries", col_name):
            print(f"[+] Adding column '{col_name}' to 'advisory_queries' table...")
            cursor.execute(f"ALTER TABLE advisory_queries ADD COLUMN {col_name} {col_type};")
        else:
            print(f"[-] Column '{col_name}' already exists in 'advisory_queries'.")

    # Create helpful indexes for fast lookup and user isolation
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_mobile ON users(mobile_number);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_nlp_user_id ON nlp_predictions(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_detections_user_id ON disease_detections(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_advisories_user_id ON advisory_queries(user_id);")

    conn.commit()
    conn.close()
    print("[SUCCESS] Phase 5 database migration completed successfully!")


if __name__ == '__main__':
    migrate()
