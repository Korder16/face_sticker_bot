from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.types.input_sticker import InputSticker
from aiogram.enums import StickerFormat
import logging


async def create_sticker_pack(message: Message, user_id, sticker_pack_name: str):

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

    logging.info("Collected all stickers")

    try:
        await message.bot.delete_sticker_set(name=sticker_pack_name)
        logging.info(
            f"deleted sticker pack with for user: {user_id}, name: {sticker_pack_name}"
        )

    except:
        logging.info("sticker pack already deleted")

    try:
        await message.bot.create_new_sticker_set(
            user_id=user_id,
            name=sticker_pack_name,
            title="title",
            stickers=stickers,
        )
    except:
        logging.info("cannot create sticker pack")
