from pydantic import BaseModel


class ReviewComment(BaseModel):
    summary: str