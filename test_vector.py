from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/knowledgevault"
)

with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS vector_test2 (
            id SERIAL PRIMARY KEY,
            embedding VECTOR(384)
        )
    """))

print("SUCCESS")