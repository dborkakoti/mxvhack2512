import os
import pandas as pd
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database Setup
DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    # Fallback or error if not found. For now, we prefer to error or warn in init generally, 
    # but at module level we just define it.
    print("WARNING: SUPABASE_DATABASE_URL not found in environment.")

# Create SQLAlchemy engine
# pool_pre_ping=True helps with connection keepalive issues
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    if not engine:
        print("Database not initialized: Missing URL.")
        return

    try:
        # Verify connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection established.")
        
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        print("Database tables verified.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_message(role: str, content: str):
    if not engine:
        return
    db = SessionLocal()
    try:
        new_message = Message(role=role, content=content)
        db.add(new_message)
        db.commit()
    except Exception as e:
        print(f"Error adding message: {e}")
        db.rollback()
    finally:
        db.close()

def get_messages():
    if not engine:
        return []
    db = SessionLocal()
    try:
        messages = db.query(Message).order_by(Message.id).all()
        return [
            {
                "role": m.role, 
                "content": m.content, 
                "timestamp": m.timestamp.isoformat() if m.timestamp else None
            } 
            for m in messages
        ]
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []
    finally:
        db.close()

def clear_messages():
    if not engine:
        return
    db = SessionLocal()
    try:
        db.query(Message).delete()
        db.commit()
    except Exception as e:
        print(f"Error clearing messages: {e}")
        db.rollback()
    finally:
        db.close()
