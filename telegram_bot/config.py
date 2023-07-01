import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pydantic import BaseSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class Settings(BaseSettings):
    BASE_API_URL: str = f"http://127.0.0.1:8000"

settings = Settings()

BASE_SERVER_URL: str = settings.BASE_API_URL

load_dotenv()
storage = MemoryStorage()
API_TOKEN: str = os.getenv("TELEBOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)

