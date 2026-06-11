from src.core.queue import review_queue
from src.core.dependencies import get_github_service, get_llm_service
from src.core.logging import logger


def process_pr_review(repo_full_name: str, pr_number: int, installation_id: int):
    github = get_github_service()
    llm = get_llm_service()

    files = github.get_pr_files(repo_full_name, pr_number, installation_id)
    diff = github.build_pr_diff(files)
    logger.info(f"Built PR diff with length: {len(diff)} characters")

    review = llm.review_pr(title="", description="", diff=diff)
    logger.info(f"Generated review comment with length: {len(review)} characters")

    github.create_pr_comment(repo_full_name, pr_number, installation_id, review)
