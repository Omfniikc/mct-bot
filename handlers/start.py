from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages

from text.messages import *
from keyboards import reply as kbr
from keyboards import inline as kbi
from fsm.states import main_menu
from db_methods.user_methods import add_user, get_user_info, add_trainer_for_user, add_trainer, set_user_name
from generate.check_time import get_current_time
from handlers.time import set_time
from handlers.pay import schedule_once_every_7_days

from middlewares.is_group import PrivateChatMiddleware
import asyncio


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    args = message.text.split(' ', 1)[1] if ' ' in message.text else None
    user_data = await get_user_info(message.from_user.id)
    await add_user(message.from_user.id, message.from_user.username)
    is_reg = 1 if user_data else 0
    await state.update_data(in_base=is_reg)
    if args:
        referrer_id = args
        if str(referrer_id) == str(message.from_user.id):
            await message.answer(REF_MESSAGES[1])
            return
        else:
            await add_trainer_for_user(message.from_user.id, args)
            trainer = await bot.get_chat(args)
            await message.answer(f"Теперь ты привязан к тренеру @{trainer.username}")
            await bot.send_message(args, f"@{message.from_user.username} теперь является вашим клиентом")
            await state.set_state(main_menu.start_user)
            user_date = await get_user_info(message.from_user.id)
            time = get_current_time(int(user_date[6]))
            await state.set_state(main_menu.user_name)
            await message.answer("Введи свое имя:")
    else:
        await state.set_state(main_menu.start)
        await message.answer(START_MESSAGES[0], reply_markup=kbi.user_or_trainer())
    

@router.callback_query(main_menu.start)
async def start_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data_s = await state.get_data()
    data = callback.data
    message = callback.message

    user_data = await get_user_info(callback.from_user.id)
    await add_user(callback.from_user.id, callback.from_user.username)
    is_reg = data_s["in_base"]

    if data == "trainer":
        await add_trainer(message.chat.id, 7)
        user_id = message.from_user.id
        bot_name = await bot.get_me()
        referral_link = f"https://t.me/{bot_name.username}?start={user_id}"
        user_date = await get_user_info(callback.from_user.id)
        time = get_current_time(int(user_date[6]))
        await message.answer(TRAINER_START_MESSAGES[1])
        await asyncio.sleep(1)
        await message.answer(TRAINER_START_MESSAGES[2])
        await asyncio.sleep(1)
        await message.answer(TRAINER_START_MESSAGES[3])
        if is_reg == 0:
            await message.answer(TRAINER_START_MESSAGES[5], reply_markup=kbr.main_menu())
            await asyncio.run(schedule_once_every_7_days(callback.from_user.id, bot))
        await asyncio.sleep(1)
        await message.answer(TRAINER_START_MESSAGES[4].format(referral_link), parse_mode="HTML")
        await asyncio.sleep(6)
        await message.answer(
            START_MESSAGES[5].format(time, user_date[6]),
            reply_markup=kbi.user_gmt(1))
        await state.set_state(main_menu.add_food)
        
    elif data == "user":
        await state.set_state(main_menu.user_name)
        await message.answer("Введи свое имя:")


@router.message(main_menu.user_name)
async def user_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer("Введи свою фамилию:")
    await state.set_state(main_menu.user_surname)


@router.message(main_menu.user_surname)
async def user_surname(message: Message, state: FSMContext):
    await state.update_data(user_surname=message.text)
    data = await state.get_data()
    await set_user_name(data["user_name"], data["user_surname"], message.from_user.id)
    await state.set_state(main_menu.start_user)
    user_date = await get_user_info(message.from_user.id)
    time = get_current_time(int(user_date[6]))
    await message.answer(START_MESSAGES[1])
    await asyncio.sleep(1)
    await message.answer(START_MESSAGES[2])
    await asyncio.sleep(6)
    await message.answer(START_MESSAGES[3])
    await asyncio.sleep(6)
    await message.answer_photo(types.FSInputFile(path='./media/img/ex2.PNG'))
    await asyncio.sleep(1)
    await message.answer(START_MESSAGES[4], reply_markup=kbr.main_menu())
    await asyncio.sleep(6)
    await message.answer(
        START_MESSAGES[5].format(time, user_date[6]),
        reply_markup=kbi.user_gmt(1))


@router.callback_query(main_menu.start_user)
async def start_2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(main_menu.add_food)
    if callback.data != "main_start":
        await set_time(callback)
    message = callback.message

    await asyncio.sleep(1)
    await message.answer(
        '''Тренер в ближайшее время задаст тебе цели по КБЖУ.

А сейчас, ты можешь отпарить первое фото, и я определю КБЖУ блюда!''',
        reply_markup=kbi.main())