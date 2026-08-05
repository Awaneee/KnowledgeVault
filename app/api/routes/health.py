from fastapi import APIRouter
from sqlalchemy import text

from app.core.redis_client import redis_client
from app.database.session import SessionLocal

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    db_status = "ok"
    redis_status = "ok"

    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
        finally:
            db.close()
    except Exception:
        db_status = "error"

    try:
        redis_client.ping()
    except Exception:
        redis_status = "error"

    overall = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    status_code = 200 if overall == "ok" else 503

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=status_code,
        content={"status": overall, "db": db_status, "redis": redis_status},
    )
