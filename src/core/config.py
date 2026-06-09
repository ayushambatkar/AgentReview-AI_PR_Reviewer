import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_app_id: str
    github_private_key_path: str
    app_name: str = "Agent Review"
    app_version: str = "0.1.0"
    groq_api_key: str
    langchain_api_key: str
    langchain_tracing_v2: bool = True
    langchain_project: str = "Agent Review"
    dev_secret: str

    class Config:
        env_file = ".env"


settings = Settings()

os.environ.setdefault("LANGCHAIN_TRACING_V2", str(settings.langchain_tracing_v2).lower())
os.environ.setdefault("LANGSMITH_TRACING_V2", str(settings.langchain_tracing_v2).lower())
os.environ.setdefault("LANGCHAIN_API_KEY", settings.langchain_api_key)
os.environ.setdefault("LANGSMITH_API_KEY", settings.langchain_api_key)
os.environ.setdefault("LANGCHAIN_PROJECT", settings.langchain_project)
os.environ.setdefault("LANGSMITH_PROJECT", settings.langchain_project)
