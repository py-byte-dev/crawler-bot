from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    file = State()
