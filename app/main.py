from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app import database
from app.chatbot import get_chatbot
import os

app = FastAPI()

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

@app.post("/api/chat")
async def chat(message: Message):
    # Save user message
    database.add_message("user", message.content)
    
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
    database.add_message(role, response_content)
    
    return {"role": role, "content": response_content}

@app.get("/api/history")
async def get_history():
    return database.get_messages()

@app.delete("/api/history")
async def clear_history():
    database.clear_messages()
    return {"message": "History cleared"}
