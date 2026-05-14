from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(BaseSettings):
    """
    Centralized application configuration.
    """

    app_env: str = "development"
    log_level: str = "INFO"

    gradio_server_port: int = 7860
    gradio_share: bool = False

    max_file_size_mb: int = 10

    github_api_key: str = ""
    github_model: str = "openai/gpt-4.1-mini"
    github_base_url: str = "https://models.github.ai/inference"

    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    openai_api_key: str = ""

    temperature: float = 0.3
    max_tokens: int = 1200

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
