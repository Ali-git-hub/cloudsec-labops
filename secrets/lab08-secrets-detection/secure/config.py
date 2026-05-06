import os

def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def get_database_url() -> str:
    return required_env("DATABASE_URL")

def get_github_token() -> str:
    return required_env("GITHUB_TOKEN")
