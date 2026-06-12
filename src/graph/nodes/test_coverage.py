import json

from src.graph.state import ReviewState
from src.services.llm_service import llm_service


def test_coverage_node(state: ReviewState):

    prompt = f"""
You are a test engineer.

Focus ONLY on:
- Missing tests
- Untested code paths
- Missing edge cases
- Missing integration tests

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
        "test_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", [])
    }