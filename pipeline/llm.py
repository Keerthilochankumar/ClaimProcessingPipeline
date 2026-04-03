import os
from dotenv import load_dotenv
from langchain_siliconflow import ChatSiliconFlow
load_dotenv()
SILICONFLOW_BASE_URL = "https://api.siliconflow.com/v1"

def get_chat_model():
    try:
        api_key = os.getenv("SILICONFLOW_API_KEY")
        model = os.getenv("SILICONFLOW_MODEL")
        if not api_key:
            raise ValueError("SILICONFLOW_API_KEY environment variable is not set.")
        if not model:
            raise ValueError("SILICONFLOW_MODEL environment variable is not set.")

        return ChatSiliconFlow(
            siliconflow_api_key=api_key,
            base_url=SILICONFLOW_BASE_URL,
            model=model
        )
    except Exception as e:
        print(f"Error initializing ChatSiliconFlow: {e}")
        raise
