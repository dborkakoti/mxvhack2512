import sqlite3
import pandas as pd
from app.database import DB_NAME

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

    try:
        conn = sqlite3.connect(DB_NAME)
        # using pandas for easy formatting
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        if df.empty:
            return "No results found."
            
        return df.to_markdown(index=False)
    except Exception as e:
        return f"Error executing query: {str(e)}"
