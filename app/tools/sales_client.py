import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# We use the same DB connection as the main app
DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def query_sales_database(sql_query: str):
    """
    Executes a read-only SQL query against the sales database and returns the results.
    
    The database contains a 'sales' table with the following columns:
    - salesperson_id (TEXT): Unique ID of the salesperson (e.g., SP01)
    - salesperson_name (TEXT): Name of the salesperson
    - territory (TEXT): Assigned territory (e.g., North, South, East, West)
    - category (TEXT): Sales category (e.g., Enterprise, SMB)
    - jan, feb, ..., dec (REAL): Monthly sales figures
    - total_revenue_inr_lakhs (REAL): Total annual revenue
    - target_revenue_inr_lakhs (INTEGER): Annual revenue target
    - deals_closed (INTEGER): Number of deals closed
    - active_days (INTEGER): Number of active working days
    - approved_leave_days (INTEGER): Number of approved leave days
    - incentive_eligible (TEXT): 'Yes' or 'No'
    
    Args:
        sql_query (str): A valid SQL query string (SELECT only).
        
    Returns:
        str: A string representation of the query results (e.g., list of rows or a markdown table).
    """
    # Basic safety check to prevent modification
    if not sql_query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries are allowed."

    if not DATABASE_URL:
        return "Error: Database URL not configured."

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            keys = result.keys()
            
            if not rows:
                return "No results found."
            
            # Format as Markdown Table manually
            header = "| " + " | ".join(keys) + " |"
            separator = "| " + " | ".join(["---"] * len(keys)) + " |"
            
            lines = [header, separator]
            for row in rows:
                # Convert row values to string and escape pipes if necessary
                row_str = "| " + " | ".join(str(val).replace("|", "&#124;") for val in row) + " |"
                lines.append(row_str)
                
            return "\n".join(lines)

    except Exception as e:
        return f"Error executing query: {str(e)}"
