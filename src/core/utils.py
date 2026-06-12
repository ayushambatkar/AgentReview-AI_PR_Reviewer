import hmac
import hashlib
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
