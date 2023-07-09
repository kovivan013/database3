from abc import ABC
import uuid
import string
import random

from database3.telegram_bot.config import API_TOKEN

class Default(ABC):

    default_callback: str = f"default_callback"
    none_callback: str = f"none_callback"

var = {"a": {"key1": "value1", "key2": "value2"}}


