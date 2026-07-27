from sqlalchemy import text

from app.database.session import engine


with engine.connect() as connection:
    db = connection.execute(
        text("SELECT current_database()")
    ).scalar()

    print("Database:", db)

    extensions = connection.execute(
        text("SELECT extname FROM pg_extension")
    ).fetchall()

    print("Extensions:")
    for ext in extensions:
        print(ext[0])