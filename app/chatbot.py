import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts/chatbot.md")
        try:
            with open(prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful assistant."

    def generate_response(self, message: str, history: list = None) -> str:
        """
        Generates a response using Gemini.
        Args:
            message: The user's current message.
            history: A list of dicts with 'role' and 'content' keys.
        """
        # Note: In a real app, we would format history for Gemini.
        # For now, we are just sending the system prompt + new message as context is handled stateless here
        # or we could construct a chat session.
        
        full_prompt = f"{self.system_prompt}\n\nUser: {message}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Singleton instance
chatbot_instance = None

def get_chatbot():
    global chatbot_instance
    if chatbot_instance is None:
        try:
            chatbot_instance = ChatBot()
        except Exception as e:
            print(f"Failed to initialize ChatBot: {e}")
            return None
    return chatbot_instance
