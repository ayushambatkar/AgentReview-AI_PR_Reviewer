import json

from src.graph.state import ReviewState
from src.core.dependencies import get_llm_service

llm_service = get_llm_service()


def quality_node(state: ReviewState):

    prompt = f"""
You are a senior software engineer reviewing a pull request.

Focus ONLY on:
- Maintainability
- Code smells
- Excessive complexity
- Poor naming
- Duplication
- Readability

Return ONLY valid JSON:

{{
  "issues": [
    "issue 1",
    "issue 2"
  ],
  "inline_comments": [
    {{
      "file": "example.py",
      "line": 12,
      "comment": "Suggestion here"
    }}
  ]
}}

If nothing is found:

{{
  "issues": [],
  "inline_comments": []
}}

PR Title:
{state["title"]}

PR Description:
{state["description"]}

Diff:
{state["diff"]}
"""

    response = llm_service.invoke(prompt)

    data = json.loads(response)

    return {
        "quality_issues": data["issues"],
        "inline_comments": data["inline_comments"],
    }