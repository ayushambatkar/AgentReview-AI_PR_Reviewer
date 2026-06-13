from typing import cast

from src.core.dependencies import (
    get_github_service,
)
from src.core.logging import logger
from src.graph.state import ReviewState
from src.graph.workflow import get_graph


def process_pr_review(
    repo_full_name: str,
    pr_number: int,
    installation_id: int,
):
    github = get_github_service()
    review_mode = github.get_review_mode(repo_full_name, installation_id)
    graph = get_graph(review_mode)

    logger.info(f"Using review mode: {review_mode}")

    pull_request = github.get_pull_request(
        repo_full_name,
        pr_number,
        installation_id,
    )

    files = github.get_pr_files(
        repo_full_name,
        pr_number,
        installation_id,
    )

    diff = github.build_pr_diff(files)

    logger.info(f"Built PR diff with length: {len(diff)} characters")

    state: ReviewState = {
        "pr_number": pr_number,
        "repo_name": repo_full_name,
        "files_changed": [file.filename for file in files],
        "diff": diff,
        "routing_flags": {},
        "security_issues": [],
        "quality_issues": [],
        "db_issues": [],
        "test_issues": [],
        "inline_comments": [],
        "title": pull_request.title,
        "description": pull_request.body or "",
        "summary": "",
    }

    result = cast(
        ReviewState,
        graph.invoke(state),
    )

    logger.info(
        "Review result counts | security=%s quality=%s db=%s test=%s inline=%s summary_len=%s",
        len(result["security_issues"]),
        len(result["quality_issues"]),
        len(result["db_issues"]),
        len(result["test_issues"]),
        len(result["inline_comments"]),
        len(result["summary"]),
    )

    if not result["summary"] and not result["inline_comments"]:
        logger.info(f"No review generated for PR #{pr_number}")
        return

    github.create_review(
        repo_full_name=repo_full_name,
        pr_number=pr_number,
        installation_id=installation_id,
        summary=result["summary"],
        inline_comments=result["inline_comments"],
    )

    logger.info(f"Posted review with {len(result['inline_comments'])} inline comments")
