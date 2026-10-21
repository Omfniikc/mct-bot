import os
import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from keyboards import reply as kbr
from keyboards import inline as kbi
from fsm.states import correct_food, main_menu
from db_methods.food_methods import correct_food_data, delete_food, food_check_daily, get_food_data
from gpt_models.scan_food import re_scan
from generate.create_table import styling
from gpt_models.voice_to_text import voice2text
from middlewares.is_subscrioption import HasSubscriptionFilter
from middlewares.is_group import PrivateChatMiddleware
from text.messages import *


router = Router()
router.message.middleware(PrivateChatMiddleware())
router.message.middleware(HasSubscriptionFilter())
logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'correct_test_data')
@router.callback_query(F.data == 'delete_test_data')
def test_delete(callback: CallbackQuery, state: FSMContext):
    print(2)


async def corect_food(message: Message, state: FSMContext, text, load_msg: Message) -> None:
    data = await state.get_data()
    msg_del_id = [data["corect_msg_for_del"], data["corect_msg_for_del"]-1]
    food_id = data["food_id"]

    food_data = await get_food_data(food_id)
    logger.debug(food_data)

    path = food_data[2].split('/')[-1][:-4]

    file_name = f"notes/{path}.txt"
    with open(file_name, "r", encoding="utf-8") as f:
        table = f.read()

    food_table = await re_scan(table, text)

    if food_data[9] == 1:
        path_img = f"downloads/img/croped/{path}.jpg"
    else:
        path_img = ""

    if food_table == "НЕТ":
        cht_id = message.chat.id
        try:
            await message.bot.delete_message(cht_id, msg_del_id[0])
            await message.bot.delete_message(cht_id, msg_del_id[1])
            await load_msg.delete()
        except Exception as e:
            logger.warning("Не удалось удалить сообщение: %s", e)
        await message.answer_photo(FSInputFile(path=f"notes/{path}.png"))
        await message.answer("Извините, но данных для изменения не достаточно", reply_markup=kbr.main())
        
        return

    data_vis = await styling(food_table, path_img, path) #+'.png'

    food_data = await correct_food_data(food_id, data_vis[0], data_vis[1])

    cht_id = message.chat.id
    try:
        await message.bot.delete_message(cht_id, msg_del_id[0])
        await message.bot.delete_message(cht_id, msg_del_id[1])
        await load_msg.delete()
    except Exception as e:
        logger.warning("Не удалось удалить сообщение: %s", e)

    data = await food_check_daily(message.from_user.id)


    goals = data[1]
    kcal_goal = int(goals[1])
    p_goal = float(goals[2])
    f_goal = float(goals[3])
    c_goal = float(goals[4])

    kcal_sum = 0
    for food_info in data[0]:
        kcal_sum += int(float(food_info[3]))

    kcal_sum = 0
    protein_sum = 0
    fat_sum = 0
    carbohydrate_sum = 0
    for food_info in data[0]:
        kcal_sum += int(float(food_info[3]))
        protein_sum += float(food_info[5])
        fat_sum += float(food_info[6])
        carbohydrate_sum += float(food_info[7])

    
    protein_sum = round(protein_sum, 2)
    fat_sum = round(fat_sum, 2)
    carbohydrate_sum = round(carbohydrate_sum, 2)

    if kcal_sum >= kcal_goal:
        mess = SEND_TABLE_MESSAGES[1].format(kcal_goal, kcal_sum, protein_sum, p_goal, fat_sum, f_goal,
                                             carbohydrate_sum, c_goal)
    else:
        mess = SEND_TABLE_MESSAGES[0].format(kcal_goal, kcal_sum, protein_sum, p_goal, fat_sum, f_goal,
                                             carbohydrate_sum, c_goal, kcal_goal - kcal_sum)


    await message.answer_photo(FSInputFile(path=food_data))
    await message.answer(mess, reply_markup=kbi.add_food(food_id))
    await state.set_state(main_menu.add_food)


@router.callback_query(lambda callback_query: 'correct_' in callback_query.data)
async def callbackTariff(callback: CallbackQuery, state: FSMContext):
    await state.set_state(correct_food.comment)
    await state.update_data(old_message=callback.message.text)
    await callback.message.edit_text(
        '🟡 ЧТОБЫ ВНЕСТИ ИЗМЕНЕНИЯ\n\n'+
        'Отправь голосовое или текстовое сообщение 👇\n'+
        'Например: на фото котлета из свинины, а не из говядины', reply_markup=kbi.cancel_redact_food())
    print(callback.data.split('_')[1])
    await state.update_data(food_id=callback.data.split('_')[1], corect_msg_for_del=callback.message.message_id)


@router.callback_query(correct_food.comment, F.data == "cancel")
async def cancel_redact_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = callback.message
    await message.edit_text(text=data["old_message"], reply_markup=kbi.add_food(data["food_id"]))


@router.callback_query(lambda callback_query: 'delete_' in callback_query.data)
async def delete_food_handler(callback: CallbackQuery):
    await callback.message.edit_text("Вы точно хотите удалить прием пищи?", reply_markup=kbi.no_del(callback.data.split('_')[1]))


@router.callback_query(lambda callback_query: 'deletetrue_' in callback_query.data)
async def true_delete_food(callback: CallbackQuery):
    await delete_food(callback.data.split('_')[1])
    cht_id = callback.message.chat.id
    msg_id = [callback.message.message_id, callback.message.message_id-1]
    await callback.message.bot.delete_message(cht_id, msg_id[1])
    await callback.message.edit_text("Запись удалена", reply_markup=kbi.main())


@router.callback_query(lambda callback_query: 'deleteno_' in callback_query.data)
async def no_delete_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(data["old_message"], reply_markup=kbi.correct_food(data["food_id"]))


@router.message(correct_food.comment, F.text)
async def redact_note(message: Message, state: FSMContext) -> None:
    load_msg = await message.answer(f'🔁 Пересчитываю')

    await corect_food(message, state, message.text, load_msg)


@router.message(correct_food.comment, F.voice)
async def redact_note(message: Message, state: FSMContext) -> None:
    load_msg = await message.answer(f'🔁 Пересчитываю')

    file_id = message.voice.file_id

    file = await message.bot.get_file(file_id)

    file_path = file.file_path
    destination = os.path.join("downloads", f"{file_id}.ogg")

    await message.bot.download_file(file_path, destination)

    text = await voice2text(destination)

    os.remove(destination)

    await corect_food(message, state, text, load_msg)
