import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Collection Tracker API"
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 5000

    # FQDN Configuration
    APP_FQDN: str = "localhost"
    BACKEND_URL: str = "http://localhost:5000"
    FRONTEND_URL: str = "http://localhost:3000"

    # Database Configuration
    MONGO_URI: str = "mongodb://localhost:27017/collection_db"
    
    # Dynamic CORS Origins using FQDN
    @property
    def CORS_ORIGINS(self) -> list[str]:
        return [
            self.FRONTEND_URL,
            f"http://{self.APP_FQDN}",
            f"https://{self.APP_FQDN}",
            "http://localhost:3000",
            "http://127.0.0.1:5000",
        ]

    # Path Settings
    BASE_DIR: Path = Path(__file__).resolve().parent

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
