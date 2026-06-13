from src.core.dependencies import get_llm_service
from src.core.utils import extract_json_object
from src.graph.smart.prompts.security import build_security_prompt
from src.graph.state import ReviewState

llm = get_llm_service()


def security_node(state: ReviewState):
    response = llm.invoke(build_security_prompt(state))
    data = extract_json_object(response)

    return {
        "security_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", []),
    }
