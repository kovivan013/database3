from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dataclasses import dataclass
from typing import Union
from database3.telegram_bot.utils.utils import Default


def default_reply_keyboard(one_time_keyboard: bool = True, resize_keyboard: bool = True, row_width: int = 2):
    return ReplyKeyboardMarkup(
        one_time_keyboard=one_time_keyboard,
        resize_keyboard=resize_keyboard,
        row_width=row_width
    )

def default_inline_keyboard(row_width: int = 2):
    return InlineKeyboardMarkup(
        row_width=row_width
    )


@dataclass(frozen=True)
class YesOrNo:

    yes: str = f"✅ Да"
    no: str = f"❌ Нет"
    cancel: str = f"🛑 Отмена"

    yes_callback: str = f"yes_callback"
    no_callback: str = f"no_callback"
    cancel_callback: str = f"cancel_callback"

    @classmethod
    def keyboard(cls) -> Union[ReplyKeyboardMarkup]:

        keyboard = default_reply_keyboard()

        keyboard.add(
            KeyboardButton(text=cls.yes),
            KeyboardButton(text=cls.no)
        )

        return keyboard

    @classmethod
    def inline_keyboard(cls) -> Union[InlineKeyboardMarkup]:

        keyboard = default_inline_keyboard()

        keyboard.add(
            InlineKeyboardButton(text=cls.yes,
                                 callback_data=cls.yes_callback),
            InlineKeyboardButton(text=cls.no,
                                 callback_data=cls.no_callback)
        )

        return keyboard

    @classmethod
    def cancel_keyboard(cls) -> Union[ReplyKeyboardMarkup]:

        keyboard = default_reply_keyboard()

        keyboard.add(
            KeyboardButton(text=cls.cancel)
        )

        return keyboard

    @classmethod
    def cancel_inline_keyboard(cls) -> Union[InlineKeyboardMarkup]:
        keyboard = default_inline_keyboard()

        keyboard.add(
            InlineKeyboardButton(text=cls.cancel,
                                 callback_data=cls.cancel_callback)
        )

        return keyboard


@dataclass(frozen=True)
class ControlMenu:

    forward: str = f"Вперёд ▶"
    backward: str = f"◀ Назад"
    close: str = f"Закрыть ✖"

    forward_callback: str = f"forward_control_callback"
    backward_callback: str = f"backward_control_callback"
    close_callback: str = f"close_control_callback"


@dataclass(frozen=True)
class StartMenu:

    classes: str = f"👨‍🎓 Мои классы"

    @classmethod
    def keyboard(cls) -> Union[ReplyKeyboardMarkup]:

        keyboard = default_reply_keyboard()

        keyboard.add(
            KeyboardButton(text=cls.classes)
        )

        return keyboard


@dataclass(frozen=True)
class ClassesMenu(Default, ControlMenu):

    create_class: str = f"➕ Создать новый класс"
    invite_link: str = f"🔗 Присоединиться к классу"

    create_class_callback: str = f"add_class_callback"
    invite_link_callback: str = f"invite_link_callback"

    keyboard_height: int = 5
    keyboard_width: int = 2
    buttons_on_page: int = keyboard_height * keyboard_width
    page_now: int = 1

    @classmethod
    def callback_handler(cls, callback: str, last_page: int):

        if callback == cls.default_callback:
            cls.page_now = 1
        elif callback == cls.forward_callback and cls.page_now < last_page:
            cls.page_now += 1
        elif callback == cls.backward_callback and cls.page_now > 1:
            cls.page_now -= 1

    @classmethod
    def keyboard(cls, callback: str = Default.default_callback, classes: dict = {}) -> Union[InlineKeyboardMarkup]:

        length = len(classes)
        keyboard = default_inline_keyboard(row_width=3)
        all_pages: int = -int(-length // cls.buttons_on_page)
        cls.callback_handler(callback=callback, last_page=all_pages)

        page_end_index: int = cls.page_now * cls.buttons_on_page
        element_now_index: int = page_end_index - cls.buttons_on_page

        classes_dict: dict = {i: {v.get("name"): v.get("id")} for i, v in enumerate(classes.values(), start=1)}

        if classes:

            keyboard.add(
                InlineKeyboardButton(text=f"Страница {cls.page_now}/{all_pages}",
                                     callback_data=cls.none_callback)
            )

            for h in range(1, cls.keyboard_height + 1):
                add_first: bool = True
                for w in range(1, cls.keyboard_width + 1):
                    element_now_index += 1
                    if add_first:
                        add_first = False
                        try:
                            keyboard.add(
                                InlineKeyboardButton(text=list(classes_dict[element_now_index].keys())[0],
                                                     callback_data=list(classes_dict[element_now_index].values())[0])
                            )
                        except:
                            break
                    else:
                        try:
                            keyboard.insert(
                                InlineKeyboardButton(text=list(classes_dict[element_now_index].keys())[0],
                                                     callback_data=list(classes_dict[element_now_index].values())[0])
                            )
                        except:
                            break

        keyboard.add(
            InlineKeyboardButton(text=cls.backward,
                                 callback_data=cls.backward_callback) if cls.page_now > 1 and classes else InlineKeyboardButton(text="",
                                                                                                                    callback_data=cls.none_callback),
            InlineKeyboardButton(text=cls.close,
                                 callback_data=cls.close_callback),
            InlineKeyboardButton(text=cls.forward,
                                 callback_data=cls.forward_callback) if cls.page_now < all_pages and classes else InlineKeyboardButton(text="",
                                                                                                                           callback_data=cls.none_callback)
        )

        keyboard.add(
            InlineKeyboardButton(text=cls.create_class,
                                 callback_data=cls.create_class_callback)
        )
        keyboard.add(
            InlineKeyboardButton(text=cls.invite_link,
                                 callback_data=cls.invite_link_callback)
        )

        return keyboard


@dataclass(frozen=True)
class InClassMenu(Default, ControlMenu):

    posts_board: str = f"📑 Доска объявлений"
    available_tasks: str = f"✍ Доступные задания"
    settings: str = f"⚙️ Настройки"

    posts_board_callback: str = f"posts_board_callback"
    available_tasks_callback: str = f"available_tasks_callback"
    settings_callback: str = f"settings_callback"

    @classmethod
    def keyboard(cls, user_role: str = "member") -> Union[InlineKeyboardMarkup]:
        keyboard = default_inline_keyboard(row_width=1)

        keyboard.add(
            InlineKeyboardButton(text=cls.posts_board,
                                 callback_data=cls.posts_board_callback),
            InlineKeyboardButton(text=cls.available_tasks,
                                 callback_data=cls.available_tasks_callback),
            InlineKeyboardButton(text=cls.settings,
                                 callback_data=cls.settings_callback)
        )

        return keyboard



