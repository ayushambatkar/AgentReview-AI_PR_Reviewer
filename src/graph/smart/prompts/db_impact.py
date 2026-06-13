from src.graph.state import ReviewState


def build_db_impact_prompt(state: ReviewState) -> str:
    return f"""
You are a DBA reviewing a pull request.

Return exactly one JSON object and nothing else.

Hard rules:
- Output must be valid JSON.
- Do not wrap the response in markdown or code fences.
- Do not add prose, explanations, headings, or bullet points.
- Do not include trailing commas.
- Do not omit required keys.
- If there are no findings, return empty arrays.

Focus only on:
- Missing indexes
- Migration risks
- Breaking schema changes
- N+1 query risks
- Expensive queries

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
