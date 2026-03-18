from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    gemini_api_key: str = Field(
        default="",
        description="Gemini API key (from GEMINI_API_KEY in .env)"
    )
    groq_api_key: str = Field(
        default="",
        description="Groq API key (from GROQ_API_KEY in .env)"
    )
    openai_api_key: str = Field(
        default="",
        description="OpenAI API key (from OPENAI_API_KEY in .env, optional)"
    )
    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key (from ANTHROPIC_API_KEY in .env, optional)"
    )

    portfolio_csv_path: str = Field(
        default="my_portfolio.csv",
        description="Portfolio CSV path (from PORTFOLIO_CSV_PATH in .env)"
    )
    vectorstore_path: str = Field(
        default="vectorstore",
        description="Vectorstore path (from VECTORSTORE_PATH in .env)"
    )

    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="CORS origins (from CORS_ORIGINS in .env)"
    )

    @field_validator("gemini_api_key", "groq_api_key", "openai_api_key", "anthropic_api_key", mode="before")
    @classmethod
    def strip_api_keys(cls, v: str) -> str:
        """Strip whitespace from API keys loaded from .env"""
        if isinstance(v, str):
            return v.strip()
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance that reads directly from .env file.
    Cached to avoid re-reading .env on every call.
    """
    return Settings()
