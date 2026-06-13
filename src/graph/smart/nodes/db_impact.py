from src.core.dependencies import get_llm_service
from src.core.utils import extract_json_object
from src.graph.smart.prompts.db_impact import build_db_impact_prompt
from src.graph.state import ReviewState

llm_service = get_llm_service()


def db_impact_node(state: ReviewState):
    data = extract_json_object(llm_service.invoke(build_db_impact_prompt(state)))

    return {
        "db_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", []),
    }
