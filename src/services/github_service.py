import base64
import time
import httpx
import jwt
from src.core.logging import logger
from src.core.review_mode import DEFAULT_REVIEW_MODE, parse_review_mode
from src.core.utils import build_review_comments
from src.models.pr_model import PullRequestFile
from src.models.pr_model import PullRequest


class GitHubService:
    def __init__(self, app_id: str, private_key: str):
        self.app_id = app_id
        self.private_key = private_key

    def _generate_jwt(self):
        private_key = self.private_key

        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + (10 * 60),
            "iss": self.app_id,
        }

        return jwt.encode(payload, private_key, algorithm="RS256")

    def get_installation_access_token(self, installation_id: int) -> str:
        jwt_token = self._generate_jwt()

        response = httpx.post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/vnd.github+json",
            },
            timeout=30,
        )
        logger.info(f"GitHub API response status: {response.status_code}")
        response.raise_for_status()
        return response.json()["token"]

    def get_pr_files(self, repo_full_name: str, pr_number: int, installation_id: int):
        access_token = self.get_installation_access_token(installation_id)
        logger.info(f"Using access token: {access_token[:20]}...")

        response = httpx.get(
            f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        logger.info(f"GitHub files API response status: {response.status_code}")
        response.raise_for_status()
        return [PullRequestFile.model_validate(item) for item in response.json()]

    def get_pull_request(
        self, repo_full_name: str, pr_number: int, installation_id: int
    ) -> PullRequest:
        access_token = self.get_installation_access_token(installation_id)

        response = httpx.get(
            f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        logger.info(f"GitHub pull request API response status: {response.status_code}")
        response.raise_for_status()
        return PullRequest.model_validate(response.json())

    def get_review_mode(self, repo_full_name: str, installation_id: int) -> str:
        access_token = self.get_installation_access_token(installation_id)

        response = httpx.get(
            f"https://api.github.com/repos/{repo_full_name}/contents/.agentreview.yml",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
            timeout=30,
        )

        if response.status_code == 404:
            logger.info("No .agentreview.yml found in repository; using fast mode")
            return DEFAULT_REVIEW_MODE

        response.raise_for_status()
        payload = response.json()

        try:
            encoded_content = payload["content"].replace("\n", "")
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")
            return parse_review_mode(decoded_content)
        except Exception as exc:
            logger.warning(
                f"Failed to parse .agentreview.yml from repository; using fast mode: {exc}"
            )
            return DEFAULT_REVIEW_MODE

    def build_pr_diff(self, files):
        MAX_TOTAL_CHARS = 8000

        chunks = []
        current = 0

        for file in files:

            patch = file.patch or ""

            if len(patch) > 2000:
                patch = patch[:2000] + "\n# PATCH TRUNCATED"

            chunk = (
                f"diff --git a/{file.filename} b/{file.filename}\n"
                f"{patch}"
            )

            if current + len(chunk) > MAX_TOTAL_CHARS:
                break

            chunks.append(chunk)
            current += len(chunk)

        return "\n\n".join(chunks)

    def create_review(
        self,
        repo_full_name: str,
        pr_number: int,
        summary: str,
        inline_comments: list,
        installation_id: int,
    ) -> None:
        token = self.get_installation_access_token(installation_id)
        inline_comments = build_review_comments(inline_comments)
        response = httpx.post(
            f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/reviews",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            json={
                "body": summary,
                "event": "COMMENT",
                "comments": inline_comments,
            },
            timeout=30,
        )
        logger.info(f"GitHub review API response status: {response.status_code}")
        logger.info(f"GitHub review API response text: {response.text}")
        response.raise_for_status()
