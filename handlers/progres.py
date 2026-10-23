from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import os
import logging

from middlewares.is_group import PrivateChatMiddleware
from keyboards import reply as kbr
from generate.create_graphics import gen_weight_weekly_graphic, gen_weight_monthly_graphic, gen_weight_quarter_graphic
from db_methods.progres import update_weight, get_all_weight, get_weekly_weight, get_monthly_weight, get_quarter_weight
from db_methods.user_methods import add_weight
from fsm.states import main_menu, WeightStates


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

router = Router()
router.message.middleware(PrivateChatMiddleware())
logger = logging.getLogger(__name__)

@router.message(F.text == "Трекер веса")
@router.message(main_menu.progres, F.text == "Неделя")
async def chek_progres_weekly(message: Message, state: FSMContext):
    await state.set_state(main_menu.progres)
    data = await get_weekly_weight(message.from_user.id)
    if data == []:
        await message.answer("Ты пока не добавлял свои данные по весу за этот промежуток", reply_markup=kbr.progres())
        return
    load_msg = await message.answer("Загружаю график...")
    data_ = {}
    dates = []
    weights = []
    for i in range(len(data)):
        dates.append("/".join(data[i][2].split("-")[::-1][:2]))
        weights.append(float(data[i][3]))
    data_["date"] = dates[::-1]
    data_["weight"] = weights[::-1]
    logger.debug(data_)
    path = await gen_weight_weekly_graphic(data_, f"downloads/{message.from_user.id}_weight_weekly.png")
    await message.answer_photo(FSInputFile(path), caption="Таблица изменения веса за неделю", reply_markup=kbr.progres())
    await load_msg.delete()
    os.remove(path)
    return


@router.message(main_menu.progres, F.text == "Месяц")
async def chek_progres_monthly(message: Message, state: FSMContext):
    await state.set_state(main_menu.progres)
    data = await get_monthly_weight(message.from_user.id)
    if data == []:
        await message.answer("Ты пока не добавлял свои данные по весу за этот промежуток", reply_markup=kbr.progres())
        return
    load_msg = await message.answer("Загружаю график...")
    data_ = {}
    dates = []
    weights = []
    for i in range(len(data)):
        dates.append("/".join(data[i][2].split("-")[::-1][:2]))
        weights.append(float(data[i][3]))
    data_["date"] = dates[::-1]
    data_["weight"] = weights[::-1]
    logger.debug(data_)
    path = await gen_weight_monthly_graphic(data_, f"downloads/{message.from_user.id}_weight_monthly.png")
    await message.answer_photo(FSInputFile(path), caption="Таблица изменения веса за месяц", reply_markup=kbr.progres())
    await load_msg.delete()
    os.remove(path)
    return


@router.message(main_menu.progres, F.text == "Квартал")
async def chek_progres_quarter(message: Message, state: FSMContext):
    await state.set_state(main_menu.progres)
    data = await get_quarter_weight(message.from_user.id)
    if data == []:
        await message.answer("Ты пока не добавлял свои данные по весу за этот промежуток", reply_markup=kbr.progres())
        return
    load_msg = await message.answer("Загружаю график...")
    data_ = {}
    dates = []
    weights = []
    for i in range(len(data)):
        dates.append("/".join(data[i][2].split("-")[::-1][:2]))
        weights.append(float(data[i][3]))
    data_["date"] = dates[::-1]
    data_["weight"] = weights[::-1]
    logger.debug(data_)
    path = await gen_weight_quarter_graphic(data_, f"downloads/{message.from_user.id}_weight_quarter.png")
    await message.answer_photo(FSInputFile(path), caption="Таблица изменения веса за квартал", reply_markup=kbr.progres())
    await load_msg.delete()
    os.remove(path)
    return
    

@router.message(main_menu.progres, F.text == "Добавить вес")
async def add_weight_handler(message: Message, state: FSMContext):
    await state.set_state(WeightStates.set_weight)
    await message.answer("Введи свой вес в килограммах с точностью до десятых", reply_markup=kbr.main())

@router.message(WeightStates.set_weight, F.text)
async def set_weight(message: Message, state: FSMContext):
    if not is_float(message.text):
        await message.answer("Пожалуйста, введи только число: ваш вес, в формате 10.0")
    else:
        await add_weight(message.text, message.from_user.id)
        await update_weight(message.from_user.id, message.text)
        await message.answer("Вес задан")
        await chek_progres_weekly(message, state)
