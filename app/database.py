import os
import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def init_db():
    """
    Initializes the database connection.
    For Supabase configuration, we assume tables are managed via migration scripts.
    This function verifies connectivity.
    """
    if not DATABASE_URL:
        print("WARNING: SUPABASE_DATABASE_URL not found. Database features will fail.")
        return

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Just test connection
            conn.execute(text("SELECT 1"))
        print("Database connection successful.")
    except Exception as e:
        print(f"Error connecting to database: {e}")

def add_message(role, content):
    if not DATABASE_URL:
        return
        
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO messages (role, content) VALUES (:role, :content)"),
                {"role": role, "content": content}
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving message: {e}")

def get_messages():
    if not DATABASE_URL:
        return []

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT role, content, timestamp FROM messages ORDER BY id ASC"))
            rows = result.fetchall()
            
            # Convert SQLAlchemy Rows to list of dicts
            messages = []
            for row in rows:
                messages.append({
                    "role": row.role,
                    "content": row.content,
                    "timestamp": str(row.timestamp)
                })
            return messages
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        return []

def clear_messages():
    if not DATABASE_URL:
        return

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM messages"))
            conn.commit()
    except Exception as e:
        print(f"Error clearing messages: {e}")
