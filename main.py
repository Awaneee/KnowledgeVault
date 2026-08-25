import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.limiter import limiter
from app.middleware.request_id import RequestIDFilter, RequestIDMiddleware
from app.api.routes import categories, notes, attachment, auth, upload, topics, intents
from app.api.routes import health as health_router

# Logging — configure once here; workers configure separately via their own basicConfig.
_request_id_filter = RequestIDFilter()
_handler = logging.StreamHandler()
_handler.addFilter(_request_id_filter)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(request_id)s] %(name)s — %(message)s",
    handlers=[_handler],
)

app = FastAPI(title="KnowledgeVault")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    # Credentials (Allow-Credentials: true) must not be combined with a wildcard
    # origin — browsers reject the response and Starlette would echo back the
    # caller's Origin, granting every site a credentialed CORS approval.
    # When an explicit origin list is configured, credentials are safe.
    allow_credentials=settings.CORS_ALLOWED_ORIGINS != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(notes.router)
app.include_router(attachment.router)
app.include_router(upload.router)
app.include_router(topics.router)
app.include_router(intents.router)

from app.api.routes.retrieve import router as retrieve_router
app.include_router(retrieve_router)

from app.api.routes.ask import router as ask_router
app.include_router(ask_router)

from app.api.routes.conversations import router as conversations_router
app.include_router(conversations_router)

from app.api.routes.agent import router as agent_router
app.include_router(agent_router)


@app.on_event("startup")
def warm_embedding_model():
    from app.core.embedding_model import embedding_model
    embedding_model.encode("")
    logging.getLogger(__name__).info("Embedding model warmed up")
