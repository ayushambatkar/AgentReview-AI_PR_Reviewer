from langchain_core.messages import HumanMessage

from src.review.prompts import PR_REVIEW_PROMPT
from src.review.state import ReviewState


def create_review_node(llm):
    def reviewer(state: ReviewState):
        prompt = PR_REVIEW_PROMPT.format(
            title=state["title"],
            description=state["description"],
            diff=state["diff"],
        )

        response = llm.invoke(
            [HumanMessage(content=prompt)]
        )

        return {
            "review": response.content
        }

    return reviewer