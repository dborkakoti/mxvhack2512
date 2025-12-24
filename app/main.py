from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app import database
from app.chatbot import get_chatbot
import os
import time
from collections import defaultdict

app = FastAPI()

# Rate limiting storage
request_counts = defaultdict(list)
RATE_LIMIT_DURATION = 60  # seconds
RATE_LIMIT_REQUESTS = 4   # requests

async def rate_limiter(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    
    # Filter out old requests
    request_counts[client_ip] = [t for t in request_counts[client_ip] if current_time - t < RATE_LIMIT_DURATION]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 2 requests per minute."
        )
    
    request_counts[client_ip].append(current_time)

# Initialize database
database.init_db()

# Initialize Chatbot
chatbot = get_chatbot()

class Message(BaseModel):
    content: str

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

@app.post("/api/chat", dependencies=[Depends(rate_limiter)])
async def chat(message: Message):
    # Save user message
    # database.add_message("user", message.content)
    
    # Generate response
    if chatbot:
        role = "assistant"
        try:
            # Pass history if needed, for now just message
            response_content = chatbot.generate_response(message.content)
        except Exception as e:
            response_content = f"Error: {str(e)}"
    else:
        role = "system"
        response_content = "Chatbot not initialized. Please check API keys."
    
    # Save bot response
    # database.add_message(role, response_content)
    
    return {"role": role, "content": response_content}

@app.get("/api/history")
async def get_history():
    return database.get_messages()

@app.delete("/api/history")
async def clear_history():
    # database.clear_messages()
    return {"message": "History cleared"}
