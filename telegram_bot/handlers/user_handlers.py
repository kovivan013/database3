from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dataclasses import dataclass
from database3.telegram_bot.classes.api_requests import UserAPI
from database3.telegram_bot.keyboards.keyboards import StartMenu, ClassesMenu
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

        dct = {'house': 5, 'guitar': 6, 'jungle': 6, 'notebook': 8, 'lion': 4, 'elephant': 8, 'dog': 3, 'flower': 6, 'banana': 6, 'ocean': 5, 'car': 3, 'ice cream': 9, 'kangaroo': 8, 'mountain': 8}

        await message.answer(text=f"Выберите нужный класс из списка:",
                             parse_mode="Markdown",
                             reply_markup=ClassesMenu.keyboard(classes=dct))

def register_user_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(
        StartMenu_Handlers.menu, commands=["start"], state=None
    )
    dp.register_message_handler(
        StartMenu_Handlers.classes_button, Text(equals=StartMenu.classes), state=None
    )