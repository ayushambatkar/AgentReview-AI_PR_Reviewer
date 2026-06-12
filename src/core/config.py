import os

from pydantic_settings import BaseSettings


env_files = {
    "dev": ".env",
    "prod": ".env.prod",
}

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
    github_private_key: str
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = ".env.prod"


settings = Settings()
