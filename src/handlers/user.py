from aiogram import Router, F
from aiogram.types import Message
from ..utils.face_swap import swap_faces
from aiogram.types import FSInputFile
from aiogram.types.input_sticker import InputSticker
from aiogram.enums import StickerFormat

import logging

user_router = Router()


@user_router.message(F.photo)
async def get_photo_id(message: Message):
    user_id = message.from_user.id

    source_filepath = f"./images/{user_id}.jpg"

    file = await message.bot.get_file(message.photo[-1].file_id)

    await message.bot.download_file(file.file_path, source_filepath)

    sticker_set_name = f"sticker_pack_{user_id}_by_dev_814244fb_bot"

    swap_faces(source_filepath, "./images/templates/", user_id)

    stickers = []
    for i in range(10):
        output_filepath = f"./images/{user_id}_{i}.jpg"
        stickers.append(
            InputSticker(
                sticker=FSInputFile(output_filepath),
                format=StickerFormat.STATIC,
                emoji_list=["☺️"],
            )
        )

    try:
        await message.bot.delete_sticker_set(name=sticker_set_name)
        logging.info(
            f"deleted sticker pack with for user: {user_id}, name: {sticker_set_name}"
        )

    except:
        logging.info("sticker pack already deleted")

    try:
        await message.bot.create_new_sticker_set(
            user_id=user_id,
            name=sticker_set_name,
            title="title",
            stickers=stickers,
        )
    except:
        logging.info("cannot create sticker pack")

    try:
        sticker_set = await message.bot.get_sticker_set(name=sticker_set_name)
        await message.answer_sticker(sticker=sticker_set.stickers[0].file_id)
        logging.info("sent sticker pack")
    except:
        logging.info(
            f"cannot find sticker pack for user: {user_id}, name: {sticker_set_name}"
        )
