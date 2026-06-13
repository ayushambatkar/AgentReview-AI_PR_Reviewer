from src.core.dependencies import get_llm_service
from src.core.utils import extract_json_object
from src.graph.smart.prompts.quality import build_quality_prompt
from src.graph.state import ReviewState

llm_service = get_llm_service()


def quality_node(state: ReviewState):
    data = extract_json_object(llm_service.invoke(build_quality_prompt(state)))

    return {
        "quality_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", []),
    }
