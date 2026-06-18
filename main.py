from fastapi import FastAPI
from app.api.routes import categories, notes, attachment, auth, upload, topics, intents

app = FastAPI(title="KnowledgeVault")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(notes.router)
app.include_router(attachment.router)
app.include_router(upload.router)
app.include_router(topics.router)
app.include_router(intents.router)
from app.api.routes.retrieve import router as retrieve_router

app.include_router(retrieve_router)
from app.api.routes.ask import (
    router as ask_router
)

app.include_router(
    ask_router
)
