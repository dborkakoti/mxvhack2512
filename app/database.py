import sqlite3
import datetime
import pandas as pd
import os
import shutil

DB_NAME = "mxv.db"
DATA_FILE = "app/dataset/Sales_Data.xlsx"

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Gets /app/app
ROOT_DIR = os.path.dirname(BASE_DIR)                  # Gets /app
DB_SOURCE = os.path.join(ROOT_DIR, "mxv.db")          # /app/mxv.db
DB_DEST = "/tmp/mxv.db"

def init_db():
    if not os.path.exists(DB_DEST):
        if os.path.exists(DB_SOURCE):
            shutil.copy2(DB_SOURCE, DB_DEST)
            print(f"Database copied to {DB_DEST}")
        else:
            print(f"WARNING: Source database not found at {DB_SOURCE}")

    conn = sqlite3.connect(DB_DEST)
    c = conn.cursor()
    
    # # Create messages table
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS messages (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         role TEXT NOT NULL,
    #         content TEXT NOT NULL,
    #         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    #     )
    # ''')
    
    # Check if sales table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
    sales_table_exists = c.fetchone()
    
    if not sales_table_exists:
        print("Importing sales data...")
        try:
            # Read Excel file
            df = pd.read_excel(DATA_FILE)
            
            # Normalize column names (lowercase, replace spaces with underscores)
            df.columns = [str(col).lower().replace(' ', '_').replace('.', '') for col in df.columns]
            
            # Write to SQLite
            df.to_sql('sales', conn, if_exists='replace', index=False)
            print("Sales data imported successfully.")
        except Exception as e:
            print(f"Error importing sales data: {e}")
            
    conn.commit()
    conn.close()

def add_message(role, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT role, content, timestamp FROM messages ORDER BY id ASC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
