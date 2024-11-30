import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.handlers.admin import admin_router
from src.handlers.user import user_router

from dotenv import load_dotenv
from os import getenv


load_dotenv()
logging.basicConfig(level=logging.INFO)


async def start_bot():
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
