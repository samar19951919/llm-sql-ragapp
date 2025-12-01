from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY:str | None = None
    NVIDIA_API_KEY :str |None = None
    PG_CONNECTION_STRING :str |None = None
    CHAT_MODEL :str ="gpt-4o"
    EMBEDDING_MODEL: str  = "text_embeddings-3-large"
    VECTOR_COLLECTION : str = "Sakila_docs"

    LOG_LEVEL :str = "INFO"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
    )

settings = Settings()