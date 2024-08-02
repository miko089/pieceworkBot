
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изменить налог/процент")],
        [KeyboardButton(text="Вычесть заработанное")],
        [KeyboardButton(text="Сбросить заработок")],
        [KeyboardButton(text="Информация обо мне")],
    ], resize_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ], resize_keyboard=True
)