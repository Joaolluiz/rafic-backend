from fastapi import FastAPI
from controller import ingest, rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAFIC - RAG Application for Industry Context")

app.include_router(ingest.router, prefix="/upload", tags=["Upload"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])

origins = [
    "http://localhost:4200"  # endereço do Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

