from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import db, userid, users
from keyboards import cancel_keyboard, keyboard
from states import Form


def init(dp: Dispatcher) -> None:
    @dp.message(F.text == "Изменить налог/процент")
    async def edit_handler(message: Message, state: FSMContext) -> None:
        await state.set_state(Form.edit_percent)
        await message.answer("Введите процент числом. Пример: 13.6", reply_markup=cancel_keyboard)

    @dp.message(F.text == "Вычесть заработанное")
    async def subtract_handler(message: Message, state: FSMContext) -> None:
        await state.set_state(Form.subtract)
        await message.answer("Введите сумму, которую хотите вычесть", reply_markup=cancel_keyboard)

    @dp.message(F.text == "Сбросить заработок")
    async def reset_handler(message: Message) -> None:
        db.update(
            TABLE='users',
            WHERE=userid == message.from_user.id,
            SET=['earned', 0]
        )
        await message.answer("Заработок сброшен!", reply_markup=keyboard)

    @dp.message(F.text == "Информация обо мне")
    async def info_handler(message: Message) -> None:
        user = users.find(userid=message.from_user.id)
        await message.answer("Процент: {:.2f}%\nНалог: {:.2f}%\nЗаработано: {:.2f} руб.".format(
            user[0][1], user[0][2], user[0][3]), reply_markup=keyboard)

    @dp.message(F.text == "Отмена")
    async def cancel_handler(message: Message, state: FSMContext) -> None:
        await state.set_state(Form.normal)
        await message.answer("Отменено!", reply_markup=keyboard)
