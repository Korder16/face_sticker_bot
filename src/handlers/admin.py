from aiogram import Router, F
from aiogram.types import Message
from os import getenv
from dotenv import load_dotenv


load_dotenv()

admin_router = Router()
admins = set(getenv("ADMIN_IDS"))


# @admin_router.message(F.from_user.id.in_(admins))
# @admin_router.message(F.photo)
# async def get_photo_id(message: Message):
#     await message.answer(message.photo[-1].file_id)


@admin_router.message(F.from_user.id.in_(admins))
@admin_router.message(F.video_note)
async def get_video_note_id(message: Message):
    await message.answer(message.video_note.file_id)


@admin_router.message(F.from_user.id.in_(admins))
@admin_router.message(F.audio)
async def get_audio_id(message: Message):
    await message.answer(message.audio.file_id)


@admin_router.message(F.from_user.id.in_(admins))
@admin_router.message(F.voice)
async def get_voice_id(message: Message):
    await message.answer(message.voice.file_id)
