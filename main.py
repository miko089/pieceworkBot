import logging
import asyncio

from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher

from handlers import command_handlers, keyboard_handlers, state_handlers

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
keyboard_handlers.init(dp)
command_handlers.init(dp)
state_handlers.init(dp)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
