from pathlib import Path
import time
from urllib import response
import httpx
import jwt
from core.logging import logger
from src.models.pr_model import PullRequestFile


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

    def build_pr_diff(self, files: list[PullRequestFile]) -> str:
        diff_chunks: list[str] = []

        for file in files:
            if file.patch:
                diff_chunks.append(
                    f"diff --git a/{file.filename} b/{file.filename}\n{file.patch}"
                )
                continue

            diff_chunks.append(
                f"diff --git a/{file.filename} b/{file.filename}\n"
                f"# No patch returned for {file.status} file"
            )

        return "\n\n".join(diff_chunks)

    def create_pr_comment(
        self,
        repo_full_name: str,
        pr_number: int,
        installation_id: int,
        comment: str,
    ) -> None:

        token = self.get_installation_access_token(installation_id)

        response = httpx.post(
            f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            json={"body": comment},
            timeout=30,
        )
        logger.info(f"GitHub comment API response status: {response.status_code}")
        logger.info(f"GitHub comment API response text: {response.text}")
        response.raise_for_status()
