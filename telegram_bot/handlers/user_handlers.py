from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dataclasses import dataclass
from database3.telegram_bot.states.states import ClassesMenu_States, InClassMenu_States
from database3.telegram_bot.classes.api_requests import UserAPI, AdminAPI
from database3.telegram_bot.keyboards.keyboards import StartMenu, ClassesMenu, InClassMenu, YesOrNo
from database3.telegram_bot.config import Dispatcher, bot
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
        async with state.proxy() as data:
            data["user_classes"] = user_classes
            await message.answer(text=f"Выберите нужный класс из списка:" if user_classes else "У Вас пока нет доступных классов...\n"
                                                                                               "Создайте свой или присоединитесь к существующему!",
                                 parse_mode="Markdown",
                                 reply_markup=ClassesMenu.keyboard(classes=user_classes))


@dataclass(frozen=True)
class ClassesMenu_Handlers:

    @classmethod
    async def create_class(cls, callback: CallbackQuery, state: FSMContext) -> None:

        await RegisterClass_Handlers.yes_or_no(callback=callback, state=state)

    @classmethod
    async def edit_pages(cls, callback: CallbackQuery, state: FSMContext) -> None:


        async with state.proxy() as data:
            user_classes: dict = dict(data["user_classes"])
        await callback.message.edit_reply_markup(reply_markup=ClassesMenu.keyboard(callback=callback.data, classes=user_classes))

    @classmethod
    async def get_class(cls, callback: CallbackQuery, state: FSMContext) -> None:

        async with state.proxy() as data:
            user_classes: dict = dict(data["user_classes"])

        if callback.data in ClassesMenu.keyboard(check_keyboard=True, classes=user_classes):
            for v in user_classes.values():
                if v.get("id") == callback.data:
                    class_name: str = v.get("name")
                    class_description: str = v.get("description")

            await InClassMenu_Handlers.menu(callback=callback, state=state, class_name=class_name, class_description=class_description)

@dataclass(frozen=True)
class RegisterClass_Handlers:

    @classmethod
    async def yes_or_no(cls, callback: CallbackQuery, state: FSMContext) -> None:

        await ClassesMenu_States.register_request.set()
        await callback.message.edit_text(text=f"*Вы действительно желаете создать новый класс?*",
                                         parse_mode="Markdown",
                                         reply_markup=YesOrNo.inline_keyboard())

    @classmethod
    async def cancel_handler(cls, callback: CallbackQuery, state: FSMContext) -> None:

        await cls.delete_last_message(message=None, state=state)
        await state.finish()
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"*Успешная отмена!*",
                               parse_mode="Markdown",
                               reply_markup=StartMenu.keyboard())

    @classmethod
    async def skip_handler(cls, callback: CallbackQuery, state: FSMContext) -> None:

        await cls.check_description(skip_check=True, message=None, state=state)

    @classmethod
    async def delete_last_message(cls, message: Message, state: FSMContext) -> None:

        try:
            await message.delete()
        except:
            pass
        try:
            async with state.proxy() as data:
                await data["ans_msg"].delete()
        except:
            pass

    @classmethod
    async def name_request(cls, callback: CallbackQuery, state: FSMContext) -> None:

        await ClassesMenu_States.name_request.set()

        async with state.proxy() as data:
            data["reg_msg"] = await callback.message.edit_text(text=f"*Введите имя для нового класс:*",
                                                               parse_mode="Markdown",
                                                               reply_markup=YesOrNo.cancel_inline_keyboard())

    @classmethod
    async def check_name(cls, message: Message, state: FSMContext) -> None:

        await cls.delete_last_message(message=message, state=state)

        async with state.proxy() as data:
            user_classes: dict = dict(data["user_classes"])
        classes_list: list = []
        user = message.from_user.id

        for v in user_classes.values():
            if v.get("owner") == user:
                classes_list.append(v.get("name"))

        async with state.proxy() as data:

            if message.text in classes_list:
                data["ans_msg"] = await bot.send_message(chat_id=message.from_user.id,
                                                         text=f"*Такое имя уже существует, попробуйте снова!*",
                                                         parse_mode="Markdown")
            else:
                if len(message.text) > 28 or "\\" in message.text or message.text in classes_list:
                    data["ans_msg"] = await bot.send_message(chat_id=message.from_user.id,
                                                             text=f"*Некорректное имя, попробуйте снова!*",
                                                             parse_mode="Markdown")
                else:
                    data["name"] = message.text
                    await cls.description_request(message=message, state=state)

    @classmethod
    async def description_request(cls, message: Message, state: FSMContext) -> None:

        await ClassesMenu_States.description_request.set()
        async with state.proxy() as data:
            await data["reg_msg"].edit_text(text=f"*Введите описание для нового класса:*",
                                            parse_mode="Markdown",
                                            reply_markup=YesOrNo.cancel_inline_keyboard(with_skip=True))

    @classmethod
    async def check_description(cls, message: Message, state: FSMContext, skip_check: bool = False) -> None:

        await cls.delete_last_message(message=message, state=state)

        if skip_check:
            await cls.finish_registration(state=state)
            return

        async with state.proxy() as data:
            if len(message.text) > 54 or "\\" in message.text:
                data["ans_msg"] = await bot.send_message(chat_id=message.from_user.id,
                                                         text=f"*Некорректное описание, попробуйте снова!*",
                                                         parse_mode="Markdown")
            else:
                data["description"] = message.text
                await cls.finish_registration(state=state)

    @classmethod
    async def finish_registration(cls, state: FSMContext) -> None:

        await ClassesMenu_States.finish_register.set()
        async with state.proxy() as data:
            await data["reg_msg"].edit_text(text=f"*Регистрация завершена, создаем класс?*",
                                            parse_mode="Markdown",
                                            reply_markup=YesOrNo.inline_keyboard())

    @classmethod
    async def register_new_class(cls, callback: CallbackQuery, state: FSMContext) -> None:

        async with state.proxy() as data:
            await UserAPI.create_class(telegram_id=callback.from_user.id,
                                       name=data.get("name"),
                                       description=data.get("description") if data.get("description") is not None else "")
            await state.finish()
            await callback.message.delete()
            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f"*Новый класс успешно создан!*",
                                   parse_mode="Markdown",
                                   reply_markup=StartMenu.keyboard())


@dataclass(frozen=True)
class InClassMenu_Handlers:

    @classmethod
    async def menu(cls, callback: CallbackQuery, state: FSMContext, class_name: str = "", class_description: str = "") -> None:

        await InClassMenu_States.menu.set()
        text: str = f"👨‍🎓 *{str.capitalize(class_name)}*\n\n"
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
    dp.register_callback_query_handler(
        RegisterClass_Handlers.name_request, Text(equals=YesOrNo.yes_callback), state=ClassesMenu_States.register_request
    )
    dp.register_callback_query_handler(
        RegisterClass_Handlers.register_new_class, Text(equals=YesOrNo.yes_callback), state=ClassesMenu_States.finish_register
    )
    dp.register_callback_query_handler(
        RegisterClass_Handlers.cancel_handler, Text(equals=YesOrNo.no_callback), state=ClassesMenu_States.register_request
    )
    dp.register_callback_query_handler(
        RegisterClass_Handlers.cancel_handler, Text(equals=YesOrNo.cancel_callback), state=ClassesMenu_States.name_request
    )
    dp.register_callback_query_handler(
        RegisterClass_Handlers.cancel_handler, Text(equals=YesOrNo.cancel_callback), state=ClassesMenu_States.description_request
    )
    dp.register_callback_query_handler(
        RegisterClass_Handlers.cancel_handler, Text(equals=YesOrNo.no_callback), state=ClassesMenu_States.finish_register
    )
    dp.register_callback_query_handler(
        RegisterClass_Handlers.skip_handler, Text(equals=YesOrNo.skip_callback), state=ClassesMenu_States.description_request
    )
    dp.register_message_handler(
        RegisterClass_Handlers.check_name, state=ClassesMenu_States.name_request
    )
    dp.register_message_handler(
        RegisterClass_Handlers.check_description, state=ClassesMenu_States.description_request
    )
