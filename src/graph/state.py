from typing import NotRequired, TypedDict


class ReviewState(TypedDict):
    pr_number: int
    repo_name: str
    
    files_changed: list
    diff: str
    
    routing_flags: dict
    
    security_issues: list
    quality_issues: list
    db_issues: list
    test_issues: list
    
    inline_comments: list
    
    summary: str
    
    title: str
    description: str | None