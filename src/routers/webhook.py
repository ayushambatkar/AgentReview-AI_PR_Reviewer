from fastapi import APIRouter, Request
from src.core.config import settings
from src.models.pr_model import PullRequestEvent
from src.core.dependencies import get_github_service, get_llm_service
from src.core.utils import check_signature_match

import hashlib
import hmac

router = APIRouter()


@router.post("/webhook")
async def github_webhook(request: Request):
    
    print("Received webhook event: ", request.headers.get("X-GitHub-Event"))  # Debug log

    # CHECK SECRET
    print("Checking signature...")  # Debug log
    signing_key = request.headers.get("X-Hub-Signature-256")
    body = await request.body()
    if signing_key is None:
        return {"ok": True}
    check_signature_match(
        signing_key=signing_key, body=body
    )  # Raises error on mismatch
    print("Signature valid.")  # Debug log

    # CHECK EVENT TYPE
    github_event = request.headers.get("X-GitHub-Event")
    if github_event != "pull_request":
        print(f"Ignoring non-PR event: {github_event}")  # Debug log
        return {"ok": True}  # Ignore non-PR events

    print("Processing pull request event...")  # Debug log
    # PROCESS PR EVENT
    pull_request = PullRequestEvent.model_validate(await request.json())
    github = get_github_service()
    if pull_request.action not in ["opened", "edited"]:
        return {"ok": True}  # Only review on open or edit actions
    print(f"Fetching files for PR #{pull_request.number} in {pull_request.repository.full_name}...")  # Debug log
    files = github.get_pr_files(
        repo_full_name=pull_request.repository.full_name,
        pr_number=pull_request.number,
        installation_id=pull_request.installation.id,
    )
    diff = github.build_pr_diff(files)
    print(f"Built diff for PR #{pull_request.number}...")  # Debug log
    llm_service = get_llm_service()
    print(f"Reviewing PR #{pull_request.number} with LLM...")  # Debug log
    llm_response = llm_service.review_pr(
        title=pull_request.pull_request.title,
        description=pull_request.pull_request.body,
        diff=diff,
    )
    
    github.create_pr_comment(
        repo_full_name=pull_request.repository.full_name,
        pr_number=pull_request.number,
        installation_id=pull_request.installation.id,
        comment=llm_response,
    )

    return {"ok": True}
