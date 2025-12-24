import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

def query_policy_documents(query: str, top_k: int = 3):
    """
    Searches the company policy documents for information relevant to the query.
    
    The policies cover topics like:
    - Travel and Expense Policy
    - Leave and Attendance
    - Disciplinary Actions
    - Sales Incentive Policy
    - Territory Reassignment
    - Performance Rating
    
    Args:
        query (str): The question or topic to search for (e.g., "What is the policy for sick leave?").
        top_k (int): Number of relevant chunks to retrieve.
        
    Returns:
        str: A concatenation of the most relevant policy text chunks.
    """
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        return "Error: PINECONE_API_KEY not found."
    
    try:
        pc = Pinecone(api_key=api_key)
        index = pc.Index("mxvtravel")
        
        # Determine if we need to embed the query locally or if Pinecone handles it (e.g., integrated inference).
        # Based on upsert.py, it seems we were using "llama-text-embed-v2" for the index.
        # If the index was set up for server-side embedding (inference), we can just query with text.
        # However, upsert.py chunked text manually. It commented out the create_index_for_model part.
        # But later we uncommented it.
        # If the index is a "Pinecone inference index", we can pass string directly if using the inference SDK or if configured.
        # Let's assume for now we need to generate embeddings or use the `query` method if it supports text directly via the model integration.
        
        # Checking upsert.py again...
        # It used: pc.create_index_for_model(..., embed={"model": "llama-text-embed-v2", ...})
        # This implies we can query with string directly if we use the inference API or if the client handles it transparency.
        # Let's try the standard query method which might expect vectors, OR look for the inference interface.
        
        # Actually, for "create_index_for_model", Pinecone handles embedding generation on the server side 
        # when we upsert records with "text" field? 
        # In upsert.py we did: dense_index.upsert_records("policy", out) containing "text".
        # So we should be able to query with text.
        
        # Search using the new inference API structure
        results = index.search(
            namespace="policy",
            query={
                "inputs": {"text": query},
                "top_k": top_k
            },
            fields=["text", "policy_type"]
        )
        
        # Format results
        response_text = ""
        for match in results.get('result', {}).get('hits', []):
            field = match.get('fields', {})
            text = field.get('text', '')
            policy = field.get('policy_type', 'Unknown Policy')
            score = match.get('score', 0)
            
            response_text += f"--- Source: {policy} (Score: {score:.2f}) ---\n{text}\n\n"
            
        return response_text if response_text else "No relevant policy information found."

    except Exception as e:
        return f"Error querying policy database: {str(e)}"
