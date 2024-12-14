from aiogram.types import Message
from aiogram.types import BufferedInputFile
from aiogram.types.input_sticker import InputSticker
from aiogram.enums import StickerFormat
import logging


async def create_sticker_pack(
    message: Message, user_id, sticker_pack_name: str, output_bytes_io: tuple
):

    stickers = []
    emojis = ("🥂", "😳", "😍", "🥲", "🥵", "🥴", "😫", "🚑", "🫡", "🤭")
    for buffer, emoji in zip(output_bytes_io, emojis):
        stickers.append(
            InputSticker(
                sticker=BufferedInputFile(buffer, filename="buffer.jpg"),
                format=StickerFormat.STATIC,
                emoji_list=[emoji],
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
