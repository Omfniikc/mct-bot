from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)

from keyboards import reply as kbr
from fsm.states import main_menu
from db_methods.user_methods import is_admin, is_trainer
from text.messages import *
from middlewares.is_group import PrivateChatMiddleware


router = Router()
router.message.middleware(PrivateChatMiddleware())


async def gen_menu(message: Message, state: FSMContext, user_id) -> None:
    await state.set_state(main_menu.add_food)
    is_a = await is_admin(user_id)
    is_t = await is_trainer(user_id)
    await message.answer(
        MAIN_MENU_MESSAGE,
        reply_markup=kbr.main_menu(is_admin=is_a, is_trainer=is_t))

@router.message(F.text == "Добавить приём пищи")
@router.message(F.text == "Остaвить")
@router.message(F.text == "Главная")
async def process(message: Message, state: FSMContext) -> None:
    await gen_menu(message, state, message.from_user.id)

@router.callback_query(main_menu.add_food, F.data == "main_start")
@router.callback_query(F.data == 'main')
async def process(callback: CallbackQuery, state: FSMContext) -> None:
    message = callback.message
    await gen_menu(message, state, callback.from_user.id)


@router.message(F.text ==  'Статистика')
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(main_menu.food_note)
    await message.answer(
        "Выберите необходимую функцию",
        reply_markup=kbr.food_book())
