from aiogram import Router, F
from aiogram.types import Message
from ..utils.face_swap import swap_faces
import io
import time

from ..utils.create_sticker_pack import create_sticker_pack

import logging

user_router = Router()


@user_router.message(F.photo)
async def get_photo_id(message: Message):

    user_id = message.from_user.id

    file_in_io = io.BytesIO()
    await message.bot.download(file=message.photo[-1].file_id, destination=file_in_io)

    await message.answer("Начинаем обработку Вашего изображения")

    sticker_pack_name = f"sticker_pack_{user_id}_by_premieronline_face_sticker_bot"

    start = time.time()
    output_bytes_io = swap_faces(file_in_io, "./images/templates/", user_id)
    end = time.time()
    print(f"swap time passed: {end - start}")

    await message.answer("Начинаем создавать стикеры")

    start = time.time()
    await create_sticker_pack(message, user_id, sticker_pack_name, output_bytes_io)
    end = time.time()
    print(f"sticker pack creation time passed: {end - start}")

    try:
        sticker_set = await message.bot.get_sticker_set(name=sticker_pack_name)
        await message.answer_sticker(sticker=sticker_set.stickers[0].file_id)
        logging.info("sent sticker pack")
    except:
        logging.info(
            f"cannot find sticker pack for user: {user_id}, name: {sticker_pack_name}"
        )
