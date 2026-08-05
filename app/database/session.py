from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# pool_size: number of persistent connections kept open.
# max_overflow: extra connections allowed above pool_size under burst load.
# pool_timeout: seconds to wait for a connection before raising.
# pool_recycle: recycle connections after this many seconds to avoid
#   stale connections being returned from the pool (e.g. after a DB
#   restart or firewall timeout). 1800s = 30 minutes is a safe default.
# Without these, SQLAlchemy uses defaults (pool_size=5, max_overflow=10)
# which can exhaust quietly under concurrent worker + API load - the
# worker creates a new session per job, and if jobs pile up faster than
# they complete, the pool fills and new jobs block indefinitely.
# echo=False in all environments: echo=True logs every SQL statement
# to stdout which is useful for debugging but creates significant noise
# in normal operation and can leak query structure in logs.
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"options": "-c statement_timeout=30000"},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
