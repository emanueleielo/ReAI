from langchain_openai import ChatOpenAI

from backend.agent.utils import get_env


def _get_model():
    API_KEY = get_env("OPENAI_API_KEY")
    return ChatOpenAI(temperature=0, model_name="gpt-4o-mini-2024-07-18", openai_api_key=API_KEY)
