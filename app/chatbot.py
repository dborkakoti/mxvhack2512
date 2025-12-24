import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from app.tools.sales_client import query_sales_database
from app.tools.policy_client import query_policy_documents

class ChatBot:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        self.tools = [query_sales_database, query_policy_documents]
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash',
            tools=self.tools
        )
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
        Generates a response using Gemini with tool use capabilities.
        """
        # We start a chat session. Automatic function calling is enabled by default in recent SDKs
        # when tools are provided in the chat.
        chat = self.model.start_chat(enable_automatic_function_calling=True)
        
        # In a real scenario, we would repopulate chat.history from the DB history.
        # For now, we prepend system prompt and simple context.
        
        full_message = f"{self.system_prompt}\n\nUser Question: {message}"
        
        try:
            response = chat.send_message(full_message)
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
