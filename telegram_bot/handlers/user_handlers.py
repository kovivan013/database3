from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dataclasses import dataclass
from database3.telegram_bot.states.states import ClassesMenu_States, InClassMenu_States
from database3.telegram_bot.classes.api_requests import UserAPI, AdminAPI
from database3.telegram_bot.keyboards.keyboards import StartMenu, ClassesMenu, InClassMenu, YesOrNo
from database3.telegram_bot.config import Dispatcher
from database3.telegram_bot.utils.utils import valid_uuid
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

        await ClassesMenu_States.menu.set()
        user_classes: dict = dict(await AdminAPI.get_user_classes(telegram_id=message.from_user.id)).get("data")
        await message.answer(text=f"Выберите нужный класс из списка:" if user_classes else "У Вас пока нет доступных классов...\n"
                                                                                           "Создайте свой или присоединитесь к существующему!",
                             parse_mode="Markdown",
                             reply_markup=ClassesMenu.keyboard(classes=user_classes))


@dataclass(frozen=True)
class ClassesMenu_Handlers:

    @classmethod
    async def create_class(cls, callback: CallbackQuery, state: FSMContext) -> None:

        await callback.message.edit_text(text=f"Вы действительно желаете новый класс?",
                                         parse_mode="Markdown",
                                         reply_markup=YesOrNo.inline_keyboard())

    @classmethod
    async def edit_pages(cls, callback: CallbackQuery, state: FSMContext) -> None:

        user_classes: dict = dict(await AdminAPI.get_user_classes(telegram_id=callback.from_user.id)).get("data")
        await callback.message.edit_reply_markup(reply_markup=ClassesMenu.keyboard(callback=callback.data, classes=user_classes))

    @classmethod
    async def get_class(cls, callback: CallbackQuery, state: FSMContext) -> None:

        user_classes: dict = dict(await AdminAPI.get_user_classes(telegram_id=callback.from_user.id)).get("data")

        if callback.data in ClassesMenu.keyboard(check_keyboard=True, classes=user_classes):
            for v in user_classes.values():
                if v.get("id") == callback.data:
                    class_name: str = v.get("name")
                    class_description: str = v.get("description")

            await InClassMenu_Handlers.menu(callback=callback, state=state, class_name=class_name, class_description=class_description)


@dataclass(frozen=True)
class InClassMenu_Handlers:

    @classmethod
    async def menu(cls, callback: CallbackQuery, state: FSMContext, class_name: str = "", class_description: str = "") -> None:

        await InClassMenu_States.menu.set()
        text: str = f"👨‍🎓 *{str.title(class_name)}*\n\n"
        await callback.message.edit_text(text=text + f"📃 {class_description}" if class_description else text,
                                         parse_mode="Markdown",
                                         reply_markup=InClassMenu.keyboard())


def register_user_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(
        StartMenu_Handlers.menu, commands=["start"], state=None
    )
    dp.register_message_handler(
        StartMenu_Handlers.classes_button, Text(equals=StartMenu.classes), state=None
    )
    dp.register_callback_query_handler(
        ClassesMenu_Handlers.edit_pages, Text(equals=ClassesMenu.forward_callback), state=ClassesMenu_States.menu
    )
    dp.register_callback_query_handler(
        ClassesMenu_Handlers.edit_pages, Text(equals=ClassesMenu.backward_callback), state=ClassesMenu_States.menu
    )
    dp.register_callback_query_handler(
        ClassesMenu_Handlers.create_class, Text(equals=ClassesMenu.create_class_callback), state=ClassesMenu_States.menu
    )
    dp.register_callback_query_handler(
        ClassesMenu_Handlers.get_class, state=ClassesMenu_States.menu
    )
