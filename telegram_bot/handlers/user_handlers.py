from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dataclasses import dataclass
from database3.telegram_bot.classes.api_requests import UserAPI, AdminAPI
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

        user_classes: dict = dict(await AdminAPI.get_user_classes(telegram_id=message.from_user.id)).get("data")
        await message.answer(text=f"Выберите нужный класс из списка:",
                             parse_mode="Markdown",
                             reply_markup=ClassesMenu.keyboard(classes=user_classes))


@dataclass(frozen=True)
class ClassesMenu_Handlers:

    @classmethod
    async def edit_pages(cls, callback: CallbackQuery, state: FSMContext) -> None:

        user_classes: dict = dict(await AdminAPI.get_user_classes(telegram_id=callback.from_user.id)).get("data")
        await callback.message.edit_reply_markup(reply_markup=ClassesMenu.keyboard(callback=callback.data, classes=user_classes))

def register_user_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(
        StartMenu_Handlers.menu, commands=["start"], state=None
    )
    dp.register_message_handler(
        StartMenu_Handlers.classes_button, Text(equals=StartMenu.classes), state=None
    )
    dp.register_callback_query_handler(
        ClassesMenu_Handlers.edit_pages, Text(equals=ClassesMenu.forward_callback), state=None
    )
    dp.register_callback_query_handler(
        ClassesMenu_Handlers.edit_pages, Text(equals=ClassesMenu.backward_callback), state=None
    )