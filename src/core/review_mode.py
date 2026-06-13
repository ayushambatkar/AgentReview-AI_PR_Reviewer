from typing import Literal, cast

ReviewMode = Literal["fast", "smart"]

DEFAULT_REVIEW_MODE: ReviewMode = "fast"


def parse_review_mode(config_text: str) -> ReviewMode:
    for raw_line in config_text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        if key.strip() != "review_mode":
            continue

        normalized_value = value.strip().strip("\"'").lower()
        if normalized_value in ("fast", "smart"):
            return cast(ReviewMode, normalized_value)

        raise ValueError("review_mode must be either 'fast' or 'smart'")

    return DEFAULT_REVIEW_MODE
