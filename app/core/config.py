from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Transport Backend"
    DATABASE_URL: str
    SECRET_KEY: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()
