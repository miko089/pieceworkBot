
from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    normal = State()
    edit_percent = State()
    edit_tax = State()
    subtract = State()