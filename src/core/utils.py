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
    if hmac.compare_digest(signing_key, expected):
        return True
    else:
        raise ValueError("Invalid signature")