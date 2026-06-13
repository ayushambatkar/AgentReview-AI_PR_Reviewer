import json
import hmac
import hashlib
import re

from src.core.config import settings


def check_signature_match(signing_key, body):
    expected = (
        "sha256="
        + hmac.new(
            settings.dev_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
    )
    if not hmac.compare_digest(signing_key, expected):
        raise ValueError("Invalid signature")

    return True


def build_review_comments(inline_comments: list[dict]) -> list[dict]:
    comments = []
    for comment in inline_comments:
        comments.append(
            {
                "path": comment["file"],
                "line": comment["line"],
                "body": comment["comment"],
            }
        )
    return comments


def extract_json_object(text: str) -> dict:
    """Extracts a JSON object from the given text, handling common formatting issues."""

    cleaned_text = text.strip()

    try:
        payload = json.loads(cleaned_text)
    except json.JSONDecodeError:
        fenced_match = re.search(
            r"```(?:json)?\s*(.*?)\s*```", cleaned_text, re.DOTALL | re.IGNORECASE
        )
        if fenced_match:
            cleaned_text = fenced_match.group(1).strip()
        else:
            start_index = cleaned_text.find("{")
            end_index = cleaned_text.rfind("}")
            if start_index != -1 and end_index != -1 and end_index > start_index:
                cleaned_text = cleaned_text[start_index : end_index + 1].strip()

        payload = json.loads(cleaned_text)

    if not isinstance(payload, dict):
        raise ValueError("LLM response must be a JSON object")

    return payload
