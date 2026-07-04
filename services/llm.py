from vertexai.generative_models import GenerativeModel
from utils.prompts import RAG_PROMPT_TEMPLATE
import logging

MODEL_NAME = "gemini-2.0-flash-001"
# MODEL_NAME = "gemini-2.5-pro"
model = GenerativeModel(MODEL_NAME)

logger = logging.getLogger(__name__)

async def generate_rag_answer(question: str, context: str) -> str:
    """Gera resposta baseada em RAG usando Gemini.

    Monta o prompt usando o template e registra o prompt final para debugging.
    """

    # montar prompt com contexto e pergunta
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    # registrar o prompt (apenas primeiras 5000 chars) para debugging
    try:
        logger.debug("RAG prompt:\n%s", prompt[:5000])
    except Exception:
        pass

    # chamada ao modelo
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.25, "max_output_tokens": 800}
    )

    # retornar texto gerado
    return getattr(response, "text", str(response))
