from fastapi import FastAPI
from app.api.routes import categories, notes, attachment, auth,upload,topics

app = FastAPI(title="KnowledgeVault")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(notes.router)
app.include_router(attachment.router)
app.include_router(upload.router)
app.include_router(topics.router)
