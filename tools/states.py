
from aiogram.dispatcher.filters.state import StatesGroup, State


class SpamState(StatesGroup):
    method = State()
    target = State()
    time = State()
    threads = State()
