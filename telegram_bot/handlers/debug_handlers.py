from database3.telegram_bot.config import Dispatcher, bot
from database3.telegram_bot.classes.api_requests import UserAPI

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

async def debug_handler(message: Message, state: FSMContext) -> None:

    username: str = message.from_user.username if message.from_user.username is not None else ""
    await UserAPI.create_user(telegram_id=message.from_user.id,
                              username=username)

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await bot.send_message(chat_id=message.chat.id,
                           text=f"Перед Вами главное меню:",
                           parse_mode="Markdown",
                           reply_markup=None)

def register_debug_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(
        debug_handler, state=["*"]
    )
