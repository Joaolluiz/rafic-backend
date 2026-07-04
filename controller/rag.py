from fastapi import APIRouter
from pydantic import BaseModel
from services.vectorstore import vector_store
import vertexai
from services.llm import generate_rag_answer

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query/")
async def rag_query(request: QueryRequest):
    try:
        # Passo 1: Buscar documentos relevantes (top-k)
        docs = vector_store.as_retriever(search_kwargs={"k": 50}).get_relevant_documents(request.question)

        # Construir contexto com metadados para citação pelo LLM
        parts = []
        for doc in docs:
            meta = doc.metadata or {}
            fname = meta.get("filename", "unknown")
            chunk = meta.get("chunk", "?")
            header = f"Arquivo: {fname} -- chunk={chunk}"
            # limite de tamanho por chunk para evitar prompts gigantes
            content = (doc.page_content or "").strip()
            parts.append(f"{header}\n{content}")

        # separar blocos para facilitar leitura pelo modelo
        context = "\n\n---\n\n".join(parts)

        answer = await generate_rag_answer(request.question, context)

        return {"question": request.question, "answer": answer}

    except Exception as e:
        return {"error": str(e)}

