from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_URL: str = "redis://redis:6379/0"

    # ------------------------------------------------------------------
    # LLM routing
    # ------------------------------------------------------------------
    # Comma-separated provider priority for ANSWER GENERATION.
    # Supported values: gemini, groq, ollama
    # Intent extraction always uses Gemini → rule-based (Groq is excluded
    # from the intent chain because schema-enforced JSON is required).
    LLM_PROVIDER_PRIORITY: str = "gemini,groq"

    # Legacy single-provider setting — kept for backward compatibility.
    # LLM_PROVIDER_PRIORITY takes precedence when set.
    LLM_PROVIDER: str = "gemini"

    LLM_TIMEOUT_SECONDS: int = 60

    # ------------------------------------------------------------------
    # Gemini
    # ------------------------------------------------------------------
    GEMINI_API_KEY: str | None = None
    GEMINI_API_BASE: str = "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_INTENT_MODEL: str = "gemini-2.0-flash"
    GEMINI_ANSWER_MODEL: str = "gemini-2.0-flash"

    # ------------------------------------------------------------------
    # Groq — secondary production provider for answer generation only.
    # https://console.groq.com/keys
    # ------------------------------------------------------------------
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_BASE: str = "https://api.groq.com/openai/v1"

    # ------------------------------------------------------------------
    # Ollama — local development only.
    # Set OLLAMA_ENABLED=true to include Ollama in the fallback chain.
    # Disabled by default so production containers never attempt a local
    # Ollama connection.
    # ------------------------------------------------------------------
    OLLAMA_ENABLED: bool = False
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_CHAT_URL: str = "http://localhost:11434/api/chat"
    OLLAMA_INTENT_MODEL: str = "phi3:mini"
    OLLAMA_TITLE_MODEL: str = "phi3:mini"
    OLLAMA_ANSWER_MODEL: str = "llama3"

    # ------------------------------------------------------------------
    # Retrieval thresholds
    # ------------------------------------------------------------------
    CATEGORY_INGEST_THRESHOLD: float = 0.28
    CATEGORY_QUERY_THRESHOLD: float = 0.55

    # Minimum hybrid score for a chunk to be included in Ask results.
    # Chunks below this score are filtered before prompt construction.
    RETRIEVAL_MIN_SCORE: float = 0.10

    # ------------------------------------------------------------------
    # Ask / cache
    # ------------------------------------------------------------------
    # TTL (seconds) for cached Ask responses. Set to 0 to disable caching.
    ASK_CACHE_TTL_SECONDS: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
