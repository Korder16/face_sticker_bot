from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..utils.face_swap import swap_faces
import io
import time

from ..utils.create_sticker_pack import create_sticker_pack

import logging

user_router = Router()


@user_router.message(F.photo)
async def make_custom_stickers(message: Message):
    user_id = message.from_user.id

    file_in_io = io.BytesIO()
    await message.bot.download(
        file=message.photo[-1].file_id, destination=file_in_io
    )

    await message.answer("Начинаем обработку Вашего изображения")

    sticker_pack_name = f"sticker_pack_{user_id}_by_premieronline_face_sticker_bot"

    output_bytes_io = swap_faces(file_in_io, "./images/templates/")

    await message.answer("Начинаем создавать стикеры")

    await create_sticker_pack(message, user_id, sticker_pack_name, output_bytes_io)

    try:
        sticker_set = await message.bot.get_sticker_set(name=sticker_pack_name)
        await message.answer_sticker(sticker=sticker_set.stickers[0].file_id)
        logging.info("sent sticker pack")

        message_tokens = (
            "Это откудова к нам такого красивого замело? Чтобы добавить весь стикерпак, просто нажмите на стикер выше 🔥",
            "Делитесь нашим ботом с друзьями и встречайте Новый год вместе с онлайн-кинотеатром PREMIER! И помните: «Какая гадость, эта ваша заливная рыба»…",
        )

        await message.answer("\n".join(message_tokens))
    except:
        logging.info(
            f"cannot find sticker pack for user: {user_id}, name: {sticker_pack_name}"
        )



@user_router.message(Command("start"))
async def start(message: Message):
    message_tokens = (
        "Рекомендации к фото:",
        "С вас: хорошее фото и подписка на @premieronline.",
        "С нас: уникальный ностальгический стикерпак.",
        "",
        "Советы для идеального результата:",
        "— Лицо должно быть хорошо видно. Томные фотографии оставим для другого случая;",
        "— Уберите лишних людей из кадра, нам нужны только вы;",
        "— Советуем снять все головные уборы и очки;",
        "— Наш бот не умеет распознавать лица животных. Так что Мурзик пока без стикерпака.",
        "",
        "Генерация фото Магия бота занимает около 3 минут. Если желающих будет ооочень много, то придется немного подождать.",
    )
    await message.answer("\n".join(message_tokens))
