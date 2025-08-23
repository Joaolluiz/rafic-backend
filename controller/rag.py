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
        # Passo 1: Buscar documentos relevantes
        docs = vector_store.as_retriever(search_kwargs={"k": 3}).get_relevant_documents(request.question)

        # Juntar o conteúdo dos documentos em um único contexto
        context = "\n".join([doc.page_content for doc in docs])
        
        answer = await generate_rag_answer(request.question, context)
        
        return {"question": request.question, "answer": answer}
    
    except Exception as e:
        return {"error": str(e)}

