import os

from dotenv import load_dotenv
from pydantic import BaseSettings

class Settings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: str = "8000"

class Database(BaseSettings):
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")

    @classmethod
    def get_db_name(cls):
        return f"postgresql//:{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"

settings = Settings()
db = Database()