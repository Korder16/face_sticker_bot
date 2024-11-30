from aiogram import Router, F
from aiogram.types import Message
from ..utils.face_swap import swap_faces
from aiogram.types import FSInputFile
import time
import logging

user_router = Router()


@user_router.message(F.photo)
async def get_photo_id(message: Message):
    user_id = message.from_user.id
    file = await message.bot.get_file(message.photo[-1].file_id)

    await message.bot.download_file(file.file_path, f"{user_id}.jpg")

    start_time = time.time()
    swap_faces(f"{user_id}.jpg", "jason.jpg", f"{user_id}_result.jpg")
    logging.info("--- %s seconds ---" % (time.time() - start_time))

    await message.answer_photo(FSInputFile(f"{user_id}_result.jpg"))
