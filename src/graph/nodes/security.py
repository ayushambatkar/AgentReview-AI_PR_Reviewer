import json


from src.core.logging import logger
from src.core.dependencies import get_llm_service
from src.core.utils import extract_json_object
from src.graph.state import ReviewState

llm = get_llm_service()


def security_node(state: ReviewState):

    prompt = f"""
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

    response = llm.invoke(prompt)
    logger.info(f"Received security node response: {response}")
    data = extract_json_object(response)
    logger.info(f"Parsed security node response: {data}")
    return {
        "security_issues": data.get("issues", []),
        "inline_comments": data.get("inline_comments", []),
    }
