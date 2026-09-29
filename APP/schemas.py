from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"

    gemini_api_key: str = ""

    # You can change this model in .env if needed.
    gemini_model: str = "gemini-2.5-flash"

    database_url: str = "sqlite:///./data/edugenie.db"

    max_input_chars: int = 12000

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()