from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis - override via REDIS_URL env var in production
    REDIS_URL: str = "redis://localhost:6379/0"

    # Ollama - override via OLLAMA_URL env var in production
    OLLAMA_URL: str = "http://localhost:11434/api/generate"

    class Config:
        env_file = ".env"


settings = Settings()
