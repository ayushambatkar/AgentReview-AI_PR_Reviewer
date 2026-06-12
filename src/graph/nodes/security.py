import json

from src.core.dependencies import get_llm_service
from src.graph.state import ReviewState

llm = get_llm_service()
def security_node(state: ReviewState):

    prompt = f"""
Review this diff for security issues.

Return JSON:

{{
  "issues": [
    "issue text"
  ],
  "inline_comments": [
    {{
      "file": "file.py",
      "line": 42,
      "comment": "comment text"
    }}
  ]
}}

Diff:
{state["diff"]}
"""

    response = llm.invoke(prompt)

    data = json.loads(response)

    return {
        "security_issues": data["issues"],
        "inline_comments": data["inline_comments"],
    }