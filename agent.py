import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import AGENT_TOOLS

# Load environment variables from the .env file
load_dotenv()


class PersonalAgent:
    """Core AI Agent powered by Google Gemini with automatic tool calling and memory."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError(
                "GEMINI_API_KEY is missing or not set! "
                "Please open your .env file and paste your actual Gemini API key."
            )

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

        # Configure the agent's behavior and attach our custom tools from tools.py
        self.config = types.GenerateContentConfig(
            system_instruction=(
                "You are a helpful, resource-savvy AI agent running locally. "
                "You have access to custom tools: "
                "1) `search_web` for looking up current information online, "
                "2) `calculate` for evaluating math expressions accurately, "
                "3) `save_note` for saving notes or summaries to a file, and "
                "4) `get_current_datetime` for checking the current local date and time. "
                "Always use the appropriate tool when needed and provide clear, concise answers."
            ),
            tools=AGENT_TOOLS,
            temperature=0.3,
        )

        # Start a persistent multi-turn chat session so the agent remembers conversation history
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=self.config,
        )

    def ask(self, user_message: str) -> str:
        """Sends a message to the agent, automatically executes any needed tools, and returns the reply."""
        try:
            response = self.chat.send_message(user_message)
            return response.text or "(No text response returned.)"
        except Exception as e:
            return f"Agent error: {e}"