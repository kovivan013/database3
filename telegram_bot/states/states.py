from aiogram.dispatcher.filters.state import State, StatesGroup

class ClassesMenu_States(StatesGroup):
    menu = State()
    name_request = State()
    description_request = State()
    finish_register = State()

class InClassMenu_States(StatesGroup):
    menu = State()
