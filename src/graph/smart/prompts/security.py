from src.graph.state import ReviewState


def build_security_prompt(state: ReviewState) -> str:
    return f"""
You are a security code reviewer.

Return exactly one JSON object and nothing else.

Hard rules:
- Output must be valid JSON.
- Do not wrap the response in markdown or code fences.
- Do not add prose, explanations, headings, or bullet points.
- Do not include trailing commas.
- Do not omit required keys.
- If there are no findings, return empty arrays.

Analyze the provided git diff and identify ONLY real security issues.

Schema:

{{
  "issues": [
    {{
      "severity": "high|medium|low",
      "issue": "short description"
    }}
  ],
  "inline_comments": [
    {{
      "file": "path/to/file",
      "line": 123,
      "comment": "security concern"
    }}
  ]
}}

If there are no findings, return exactly:

{{
  "issues": [],
  "inline_comments": []
}}

Git Diff:
{state["diff"]}
"""
