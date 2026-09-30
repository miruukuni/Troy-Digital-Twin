from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://localhost:5432/personal_digital_twin"
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_classifier_model: str = "gpt-4o-mini"
    embedding_dimensions: int = 1536

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
