from langchain_groq import ChatGroq
from pydantic import SecretStr

from src.review.graph import build_review_graph
from src.core.config import settings

class LLMService:

    def __init__(self):

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=SecretStr(settings.groq_api_key)
        )

        self.graph = build_review_graph(
            llm
        )

    def review_pr(
        self,
        title: str,
        description: str | None,
        diff: str,
    ) -> str:

        result = self.graph.invoke(
            {
                "title": title,
                "description": description,
                "diff": diff,
                
            }
        )

        return result["review"]
    
llm_service = LLMService()