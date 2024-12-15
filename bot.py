import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.handlers.admin import admin_router
from src.handlers.user import user_router

from src.utils.face_swap import prepare_swapper
from src.middlewares.face_swapper import FaceSwapperMiddleware

from dotenv import load_dotenv
from os import getenv


load_dotenv()
logging.basicConfig(level=logging.INFO)


async def start_bot():
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()

    swapper, app, loaded_r = prepare_swapper("./images/templates/")

    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.update.middleware.register(FaceSwapperMiddleware(swapper, app, loaded_r))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
