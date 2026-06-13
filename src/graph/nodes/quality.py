import json

from src.graph.state import ReviewState
from src.core.dependencies import get_llm_service
from src.core.utils import extract_json_object

llm_service = get_llm_service()


def quality_node(state: ReviewState):

    prompt = f"""
You are a senior software engineer reviewing a pull request.

Return exactly one JSON object and nothing else.

Hard rules:
- Output must be valid JSON.
- Do not wrap the response in markdown or code fences.
- Do not add prose, explanations, headings, or bullet points.
- Do not include trailing commas.
- Do not omit required keys.
- If there are no findings, return empty arrays.

Schema:

{{
  "issues": ["issue 1", "issue 2"],
  "inline_comments": [
    {{
      "file": "example.py",
      "line": 12,
      "comment": "Suggestion here"
    }}
  ]
}}

If there are no findings, return exactly:

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

    data = extract_json_object(response)

    return {
    "quality_issues": data.get("issues", []),
    "inline_comments": data.get("inline_comments", []),
    }