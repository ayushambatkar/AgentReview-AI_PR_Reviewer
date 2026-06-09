from functools import lru_cache
from src.core.config import settings
from src.services.github_service import GitHubService
from src.services.llm_service import LLMService


@lru_cache()
def get_github_service():
    return GitHubService(
        app_id=settings.github_app_id,
        private_key_path=settings.github_private_key_path,
    )


@lru_cache()
def get_llm_service():
    return LLMService()
