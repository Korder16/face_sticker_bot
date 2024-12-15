from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ChatMemberBanned, ChatMemberLeft
from ..utils.face_swap import swap_faces
import io

from ..utils.create_sticker_pack import create_sticker_pack

import logging

user_router = Router()

only_private_chat = F.chat.func(lambda chat: chat.type in {"private"})


@user_router.message(F.document, only_private_chat)
async def get_file(message: Message):
    await message.answer(
        "Кажется, вы прислали фото файлом или в слишком высоком разрешении. Попробуйте прислать фото картинкой!"
    )


@user_router.message(F.photo, only_private_chat)
async def make_custom_stickers(message: Message, swapper, app, loaded_r):
    if await is_user_subscribed(message):
        user_id = message.from_user.id

        file_in_io = io.BytesIO()
        await message.bot.download(file=message.photo[-1].file_id, destination=file_in_io)

        await message.answer("Начинаем обработку Вашего изображения")

        sticker_pack_name = f"sticker_pack_{user_id}_by_premier_stikerbot"

        output_bytes_io = swap_faces(
            file_in_io, "./images/templates/", swapper, app, loaded_r
        )

        await message.answer("Начинаем создавать стикеры")

        await create_sticker_pack(message, user_id, sticker_pack_name, output_bytes_io)

        try:
            sticker_set = await message.bot.get_sticker_set(name=sticker_pack_name)
            await message.answer_sticker(sticker=sticker_set.stickers[0].file_id)
            logging.info("sent sticker pack")

            message_tokens = (
                "Это откудова к нам такого красивого замело?",
                "",
                "Чтобы добавить весь стикерпак, просто нажмите на стикер выше 🔥",
                "Делитесь нашим ботом с друзьями и встречайте Новый год вместе с онлайн-кинотеатром PREMIER!",
                "И помните: «Какая гадость, эта ваша заливная рыба»…",
            )

            await message.answer("\n".join(message_tokens))
        except:
            logging.info(
                f"cannot find sticker pack for user: {user_id}, name: {sticker_pack_name}"
            )
    else:
        await message.answer('Семёёён Семёныч! Хотели обойти систему? Подпишитесь, пожалуйста на @premieronline🥺👉🏻👈🏻')

async def is_user_subscribed(message: Message):
    chat_id = -1001189635505
    member_status = await message.bot.get_chat_member(
        chat_id=chat_id, user_id=message.from_user.id
    )
    return member_status.status not in {ChatMemberBanned, ChatMemberLeft}


@user_router.message(Command("start"), only_private_chat)
async def start(message: Message):
    if await is_user_subscribed(message):
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
            "Магия бота занимает около 3 минут. Если желающих будет ооочень много, то придется немного подождать.",
        )
        await message.answer("\n".join(message_tokens))

    else:
        await message.answer('Семёёён Семёныч! Хотели обойти систему? Подпишитесь, пожалуйста на @premieronline🥺👉🏻👈🏻')