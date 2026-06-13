from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from pydantic import SecretStr

from src.core.config import settings
from src.core.logging import logger

EMPTY_RESPONSE = """
{
    "issues": [],
    "inline_comments": []
}
"""


class LLMService:

    def __init__(self):

        self.smart_model = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=SecretStr(settings.groq_api_key),
        )

        self.fast_model = ChatGroq(
            model="llama-3.1-8b-instant", api_key=SecretStr(settings.groq_api_key)
        )

    def invoke(self, prompt: str, use_fast_model: bool = False) -> str:

        if use_fast_model:
            models = [self.fast_model]
        else:
            models = [self.smart_model, self.fast_model]

        for m in models:

            try:
                response = m.invoke([HumanMessage(content=prompt)])

                logger.info(f"Response generated using {m.model_name}")

                return str(response.content)

            except Exception as e:

                logger.warning(f"{m.model_name} failed: {e}")

        return EMPTY_RESPONSE


llm_service = LLMService()
