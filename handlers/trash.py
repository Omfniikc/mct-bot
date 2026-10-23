from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from middlewares.is_group import PrivateChatMiddleware
from keyboards import inline as kbi


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text)
async def trash_text_handler(message: Message) -> None:
    await message.answer("Извините, но я вас не понимаю, перейдите в главное меню", reply_markup=kbi.main())


@router.message(F.voice)
async def trash_voice_handler(message: Message) -> None:
    await message.answer("Извините, но я не могу воспринимать голосовые сообщения")


@router.message(F.photo)
async def trash_photo_handler(message: Message) -> None:
    await message.answer("Извините, но я не понимаю вас, если хотите добавить прием пищи, то перейдите в главное меню", reply_markup=kbi.main())


@router.message(F.video)
async def trash_video_handler(message: Message) -> None:
    await message.answer("ИЗвините, но я не могу воспринимать видео")


@router.message(F.file)
async def trash_file_handler(message: Message) -> None:
    await message.answer("ИЗвините, но я не могу воспринимать файлы")
