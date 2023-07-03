from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dataclasses import dataclass
from database3.telegram_bot.classes.api_requests import UserAPI
from database3.telegram_bot.keyboards.keyboards import StartMenu
from database3.telegram_bot.config import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

@dataclass(frozen=True)
class StartMenu_Handlers:

    @classmethod
    async def menu(cls, message: Message, state: FSMContext) -> None:

        username: str = message.from_user.username if message.from_user.username is not None else ""
        await UserAPI.create_user(telegram_id=message.from_user.id,
                                  username=username)

        await message.answer(text=f"*Главное меню:*",
                             parse_mode="Markdown",
                             reply_markup=StartMenu.keyboard())

    @classmethod
    async def classes_button(cls, message: Message, state: FSMContext) -> None:

        pass

def register_user_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(
        StartMenu_Handlers.menu, commands=["start"], state=None
    )