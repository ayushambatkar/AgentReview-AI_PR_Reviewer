import json

from src.graph.state import ReviewState
from src.core.dependencies import get_llm_service

llm_service = get_llm_service()

def db_impact_node(state: ReviewState):

    prompt = f"""
You are a DBA reviewing a pull request.

Focus ONLY on:
- Missing indexes
- Migration risks
- Breaking schema changes
- N+1 query risks
- Expensive queries

Return ONLY valid JSON:

{{
  "issues": [],
  "inline_comments": []
}}

Diff:
{state["diff"]}
"""

    data = json.loads(llm_service.invoke(prompt))

    return {
        "db_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", [])
    }