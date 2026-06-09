from typing import NotRequired, TypedDict


class ReviewState(TypedDict):
    title: str
    description: str | None
    diff: str

    review: NotRequired[str]