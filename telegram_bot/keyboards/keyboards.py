from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dataclasses import dataclass
from database3.telegram_bot.utils.utils import Default
from typing import Union


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
class StartMenu:

    classes: str = f"👨‍🎓 Мои классы"

    @classmethod
    def keyboard(cls) -> Union[ReplyKeyboardMarkup]:

        keyboard = default_reply_keyboard()

        keyboard.add(
            KeyboardButton(text=cls.classes)
        )

        return keyboard