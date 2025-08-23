from vertexai.generative_models import GenerativeModel, Part
from utils.prompts import RAG_PROMPT_TEMPLATE

MODEL_NAME = "gemini-2.0-flash-001"
model = GenerativeModel(MODEL_NAME)

async def generate_rag_answer(question: str, context: str) -> str:
    """Gera resposta baseada em RAG usando Gemini."""
    
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
    
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.3, "max_output_tokens": 512}
    )
    return response.text
