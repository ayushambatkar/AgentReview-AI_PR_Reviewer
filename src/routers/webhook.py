from fastapi import APIRouter, Request
from src.core.config import settings
from src.models.pr_model import PullRequestEvent
from src.core.dependencies import get_github_service, get_llm_service
import hashlib
import hmac

router = APIRouter()


@router.post("/webhook")
async def github_webhook(request: Request):

    # CHECK SECRET
    signing_key = request.headers.get("X-Hub-Signature-256")
    if signing_key is None:
        return {"ok": True}
    body = await request.body()
    expected = (
        "sha256="
        + hmac.new(
            settings.dev_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
    )

    if not hmac.compare_digest(signing_key, expected):
        return {"ok": True}  # Ignore invalid signatures

    github_event = request.headers.get("X-GitHub-Event")
    if github_event != "pull_request":
        return {"ok": True}  # Ignore non-PR events

    pull_request = PullRequestEvent.model_validate(await request.json())
    github = get_github_service()
    if pull_request.action not in ["opened", "edited"]:
        return {"ok": True}  # Only review on open or edit actions

    files = github.get_pr_files(
        repo_full_name=pull_request.repository.full_name,
        pr_number=pull_request.number,
        installation_id=pull_request.installation.id,
    )
    diff = github.build_pr_diff(files)
    llm_service = get_llm_service()

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
