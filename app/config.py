"""Application configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Rent a Car API"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./rent_a_car.db"

    class Config:
        env_file = ".env"


settings = Settings()
