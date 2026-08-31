import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
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

# Prometheus: auto-instrument all routes → exposes GET /metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False)

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
    # Model loads lazily on first use to avoid OOM on memory-constrained hosts.
    logging.getLogger(__name__).info("Startup complete — embedding model will load on first use")


@app.on_event("startup")
def start_inprocess_note_worker():
    """Spawn the note-processing worker as a background thread.

    We run the worker in-process (rather than a separate Railway service) to
    keep the free-tier deployment single-container. Uses a daemon thread so
    it dies with the API. The worker itself is a blocking loop that polls
    Redis for jobs; putting it on a background thread means it doesn't block
    the event loop.
    """
    import threading
    from app.workers.note_worker import main as worker_main

    log = logging.getLogger(__name__)

    def _run():
        try:
            worker_main()
        except Exception:
            log.exception("in-process note worker crashed")

    t = threading.Thread(target=_run, name="note-worker", daemon=True)
    t.start()
    log.info("in-process note worker started on thread=%s", t.name)
