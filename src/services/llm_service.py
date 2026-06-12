from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from pydantic import SecretStr

from src.core.config import settings


class LLMService:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", api_key=SecretStr(settings.groq_api_key)
        )


    def invoke(self, prompt: str) -> str:

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return str(response.content)


llm_service = LLMService()
