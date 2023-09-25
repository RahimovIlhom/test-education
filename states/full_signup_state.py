from aiogram.dispatcher.filters.state import StatesGroup, State


class FullSignupState(StatesGroup):
    register = State()
    email = State()
    birthday = State()
    confirm = State()
