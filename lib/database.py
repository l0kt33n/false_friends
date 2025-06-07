# lib/database.py
import psycopg2
from .config import DB_CONFIG

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Initializes the database, creating the necessary tables and indexes."""
    print(f"Initializing database '{DB_CONFIG['dbname']}'...")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS words")
                cursor.execute("""
                    CREATE TABLE words (
                        id SERIAL PRIMARY KEY,
                        language VARCHAR(50) NOT NULL,
                        word TEXT NOT NULL,
                        definition TEXT NOT NULL
                    )
                """)
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_lang_word ON words (language, word)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_word ON words (word)")
        print("Database initialized successfully.")
    except psycopg2.OperationalError as e:
        print(f"\n--- DATABASE CONNECTION ERROR ---")
        print(f"Could not connect to the PostgreSQL database. Is it running?")
        print(f"Please run 'docker-compose up -d' in your terminal.")
        print(f"Error details: {e}")
        raise
