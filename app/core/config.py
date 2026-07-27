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
    # Phase 2 category pipeline feature flags
    # All default to True (new behaviour). Set False to revert to Phase 1.
    # ------------------------------------------------------------------

    # Adaptive cap: max categories scales with corpus size instead of a
    # hard constant.  When False, MAX_CATEGORIES_PER_USER (50) is used.
    CATEGORY_ADAPTIVE_CAP_ENABLED: bool = True
    # One category per N notes (floor / ceiling apply below).
    CATEGORY_NOTES_PER_CAP: int = 10
    # Absolute minimum categories regardless of corpus size.
    CATEGORY_ADAPTIVE_CAP_MIN: int = 50
    # Absolute maximum categories per user (prevents UI overload at 100K notes).
    CATEGORY_ADAPTIVE_CAP_MAX: int = 2000

    # Fuzzy-compatible reuse: _compatible() checks intent_type + actor only.
    # When False, the old exact topic-string equality check is restored
    # (which makes vector reuse structurally unreachable, per ADR-002).
    CATEGORY_FUZZY_COMPAT_ENABLED: bool = True

    # Per-intent-type reuse distance thresholds (cosine distance, lower = stricter).
    # "Precise" applies to study/reference/question where topic specificity matters.
    # "Broad" applies to idea/general/event/reminder/todo where overlap is acceptable.
    CATEGORY_REUSE_THRESHOLD_PRECISE: float = 0.30
    CATEGORY_REUSE_THRESHOLD_BROAD: float = 0.40

    # Conservative general-intent category creation: validates the LLM-extracted
    # topic before creating a new general category.  Prevents single-word verbs
    # ("Added", "Create") and question fragments ("Does Redis Eviction") from
    # becoming singleton categories.  When False, all general topics create freely.
    CATEGORY_CONSERVATIVE_GENERAL_ENABLED: bool = True

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
