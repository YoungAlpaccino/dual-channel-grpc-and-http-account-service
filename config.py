"""
Settings (sketch).
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url:    str = "postgresql+asyncpg://demo:demo@localhost:5432/accounts"
    grpc_port: int = 50051
    http_port: int = 8080
    debug:     bool = False

    class Config:
        env_file = ".env"


settings = Settings()
