from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import users, db, userid
from keyboards import keyboard, cancel_keyboard
from states import Form


def init(dp: Dispatcher) -> None:
    @dp.message(Form.normal)
    async def normal_handler(message: Message) -> None:
        user = users.find(userid=message.from_user.id)
        if len(user) == 0:
            users.insert(userid=message.from_user.id, percent=100, tax=0, earned=0)
        try:
            amount = float(message.text)
        except ValueError:
            await message.answer("Пожалуйста, отправьте мне число. Например: 956.17")
            return
        today = amount * (
                1 - users.find(userid=message.from_user.id)[0][2] / 100) * users.find(userid=message.from_user.id)[0][
                    1] / 100
        db.update(
            TABLE='users',
            WHERE=userid == message.from_user.id,
            SET=['earned', today + users.find(userid=message.from_user.id)[0][3]]
        )

        await message.answer("Успешно добавлено! Сегодня вы заработали {:.2f} руб.\n\nВсего {:.2f} руб.".format(
            today, users.find(userid=message.from_user.id)[0][3]), reply_markup=keyboard)

    @dp.message(Form.edit_percent)
    async def edit_percent_handler(message: Message, state: FSMContext) -> None:
        try:
            percent = float(message.text)
        except ValueError:
            await message.answer("Пожалуйста, отправьте мне число. Например: 15", reply_markup=keyboard)
            await state.set_state("normal")
            return
        db.update(
            TABLE='users',
            WHERE=userid == message.from_user.id,
            SET=['percent', percent]
        )
        await state.set_state(Form.edit_tax)
        await message.answer("Процент изменен! Перейдем к налогу, введите число", reply_markup=cancel_keyboard)

    @dp.message(Form.edit_tax)
    async def edit_tax_handler(message: Message, state: FSMContext) -> None:
        try:
            tax = float(message.text)
        except ValueError:
            await message.answer("Пожалуйста, отправьте мне число. Например: 15", reply_markup=keyboard)
            await state.set_state("normal")
            return
        db.update(
            TABLE='users',
            WHERE=userid == message.from_user.id,
            SET=['tax', tax]
        )
        await state.set_state(Form.normal)
        await message.answer("Налог изменен!", reply_markup=keyboard)

    @dp.message(Form.subtract)
    async def subtract_handler(message: Message, state: FSMContext) -> None:
        try:
            amount = float(message.text)
        except ValueError:
            await message.answer("Пожалуйста, отправьте мне число. Например: 956.17", reply_markup=keyboard)
            await state.set_state("normal")
            return
        db.update(
            TABLE='users',
            WHERE=userid == message.from_user.id,
            SET=['earned', users.find(userid=message.from_user.id)[0][3] - amount]
        )
        await state.set_state(Form.normal)
        await message.answer("Успешно вычтено!", reply_markup=keyboard)
