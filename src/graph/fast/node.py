import json

from src.core.utils import extract_json_object
from src.graph.state import ReviewState
from src.services.llm_service import llm_service


def build_fast_review_prompt(state: ReviewState) -> str:
    review_payload = {
        "pr_number": state["pr_number"],
        "repo_name": state["repo_name"],
        "files_changed": state["files_changed"],
        "diff": state["diff"],
        "routing_flags": state["routing_flags"],
        "security_issues": state["security_issues"],
        "quality_issues": state["quality_issues"],
        "db_issues": state["db_issues"],
        "test_issues": state["test_issues"],
        "inline_comments": state["inline_comments"],
        "summary": state["summary"],
        "title": state["title"],
        "description": state["description"],
    }

    return f"""
You are a pull request reviewer.

Review the provided state in one pass and return exactly one JSON object.

Hard rules:
- Output must be valid JSON only.
- Do not wrap the response in markdown or code fences.
- Do not include explanations, prose, headings, or bullet points.
- Do not include trailing commas.
- Do not add keys that are not listed in the schema.
- If there are no findings, return empty arrays and an empty summary.

Input JSON:
{json.dumps(review_payload, ensure_ascii=False, indent=2)}

Return this exact schema:
{{
  "security_issues": [
    {{
      "severity": "high|medium|low",
      "issue": "short description"
    }}
  ],
  "quality_issues": ["issue 1", "issue 2"],
  "db_issues": ["issue 1", "issue 2"],
  "test_issues": ["issue 1", "issue 2"],
  "inline_comments": [
    {{
      "file": "path/to/file",
      "line": 123,
      "comment": "review comment"
    }}
  ],
  "summary": "short markdown summary"
}}

If there are no findings, return exactly:
{{
  "security_issues": [],
  "quality_issues": [],
  "db_issues": [],
  "test_issues": [],
  "inline_comments": [],
  "summary": ""
}}
"""


def fast_review_node(state: ReviewState):
    prompt = build_fast_review_prompt(state)
    data = extract_json_object(llm_service.invoke(prompt, use_fast_model=True))

    return {
        "security_issues": data.get("security_issues", []),
        "quality_issues": data.get("quality_issues", []),
        "db_issues": data.get("db_issues", []),
        "test_issues": data.get("test_issues", []),
        "inline_comments": data.get("inline_comments", []),
        "summary": data.get("summary", ""),
    }
