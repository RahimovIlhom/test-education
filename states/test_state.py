from aiogram.dispatcher.filters.state import StatesGroup, State


class TestStateGroup(StatesGroup):
    photo = State()
    question = State()
    response = State()
    response1 = State()
    response2 = State()
    response3 = State()
    confirm = State()
