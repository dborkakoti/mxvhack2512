import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")
DATA_FILE = "app/dataset/Sales_Data.xlsx"

if not DATABASE_URL:
    print("Error: SUPABASE_DATABASE_URL not found in .env")
    exit(1)

# Fix for sqlalchemy uri if starts with postgres:// (needs postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def migrate():
    print("Connecting to Supabase...")
    engine = create_engine(DATABASE_URL)
    
    # 1. Create Messages Table
    print("Creating messages table...")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()
    
    # 2. Upload Sales Data
    if os.path.exists(DATA_FILE):
        print(f"Reading sales data from {DATA_FILE}...")
        df = pd.read_excel(DATA_FILE)
        
        # Normalize columns
        df.columns = [str(col).lower().replace(' ', '_').replace('.', '') for col in df.columns]
        
        print("Uploading sales data to Supabase...")
        # using replace to ensure clean slate for hackathon data
        df.to_sql('sales', engine, if_exists='replace', index=False)
        print("Sales data uploaded successfully.")
    else:
        print(f"Warning: Data file {DATA_FILE} not found.")

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
