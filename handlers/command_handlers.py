from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import users
from keyboards import keyboard
from states import Form


def init(dp: Dispatcher) -> None:
    @dp.message(CommandStart())
    async def start_handler(message: Message, state: FSMContext) -> None:
        await state.set_state(Form.normal)
        user = users.find(userid=message.from_user.id)
        if len(user) == 0:
            users.insert(userid=message.from_user.id, percent=100, tax=0, earned=0)
        print(user)
        await message.answer("Привет! Я бот для учета заработанных денег! " +
                             "Просто отправь мне сумму и я прибавлю её к твоему заработку. " +
                             "Также ты можешь изменить налог или процент, вычесть заработанное или сбросить заработок.",
                             reply_markup=keyboard)
