import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

def get_chat_model():
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
        if not model:
            raise ValueError("OPENROUTER_MODEL environment variable is not set.")

        return ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=OPENROUTER_BASE_URL,
            model_name=model,
            temperature=0.9,
        )
    except Exception as e:
        print(f"Error initializing ChatOpenAI: {e}")
        raise
