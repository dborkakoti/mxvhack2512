from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app import database
import os

app = FastAPI()

# Initialize database
database.init_db()

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
    
    # Generate response (placeholder)
    response_content = "hello"
    
    # Save bot response
    database.add_message("assistant", response_content)
    
    return {"role": "assistant", "content": response_content}

@app.get("/api/history")
async def get_history():
    return database.get_messages()

@app.delete("/api/history")
async def clear_history():
    database.clear_messages()
    return {"message": "History cleared"}
