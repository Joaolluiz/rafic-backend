from fastapi import FastAPI
from controller import ingest, rag

app = FastAPI(title="RAFIC - RAG Application for Industry Context")

app.include_router(ingest.router, prefix="/upload", tags=["Upload"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])

