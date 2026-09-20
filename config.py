from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    AI_API_KEY: str = ""

    AI_MODEL: str = ""

    DATABASE_URL: str = "sqlite:///./career_chatbot.db"

    DEMO_MODE: bool = True

    UPLOAD_DIR: str = "uploads"

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024

    class Config:
        env_file = ".env"


settings = Settings()
