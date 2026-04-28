from aiogram.fsm.state import StatesGroup, State


class EventManagerSG(StatesGroup):
    type = State()
    date = State()
    time = State()
    description = State()
    preview = State()