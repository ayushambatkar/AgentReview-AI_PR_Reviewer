from src.graph.state import ReviewState
from src.services.llm_service import llm_service
from src.core.utils import extract_json_object


def test_coverage_node(state: ReviewState):

    prompt = f"""
You are a test engineer.

Return exactly one JSON object and nothing else.

Hard rules:
- Output must be valid JSON.
- Do not wrap the response in markdown or code fences.
- Do not add prose, explanations, headings, or bullet points.
- Do not include trailing commas.
- Do not omit required keys.
- If there are no findings, return empty arrays.

Focus only on:
- Missing tests
- Untested code paths
- Missing edge cases
- Missing integration tests

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

Diff:
{state["diff"]}
"""

    data = extract_json_object(llm_service.invoke(prompt))

    return {
        "test_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", []),
    }
