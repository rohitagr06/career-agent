from agents import OpenAIChatCompletionsModel
from google import genai
from openai import AsyncOpenAI

from config.settings import settings

github_clients = AsyncOpenAI(
    base_url=settings.github_base_url,
    api_key=settings.github_api_key,
    max_retries=0,
)

github_model = OpenAIChatCompletionsModel(
    model=settings.github_model, openai_client=github_clients
)

gemini_client = genai.Client(api_key=settings.google_api_key)
