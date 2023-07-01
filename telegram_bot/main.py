from aiogram import executor
from config import bot, dp

async def on_startup(_) -> None:
    print("bot started")


async def on_shutdown(_) -> None:
    print("bot shutdown")

def start_bot() -> None:
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)

if __name__ == "__main__":
    start_bot()
