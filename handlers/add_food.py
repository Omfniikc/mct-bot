from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

from keyboards import inline as kbi
from keyboards import reply as kbr
from gpt_models import scan_food as vm
from generate.create_table import styling
from fsm.states import main_menu
from db_methods.food_methods import add_food_to_table, update_last_food_time, food_check_daily
from gpt_models.voice_to_text import voice2text
from middlewares.is_subscrioption import HasSubscriptionFilter
from middlewares.is_group import PrivateChatMiddleware
from text.messages import *

import base64
import os
import pytz
import datetime
import logging
import traceback

from config import *
TOKEN = TG_TOKEN


router = Router()
all_router = Router()
router.message.middleware(PrivateChatMiddleware())
router.message.middleware(HasSubscriptionFilter())
all_router.message.middleware(HasSubscriptionFilter())
logger = logging.getLogger(__name__)


async def create_table(message: Message, answer, load_msg: Message, state: FSMContext, bot: Bot, food_irl = ''):
    if food_irl == '':
        utc_now = datetime.datetime.now(pytz.utc)
        date = str(utc_now).replace(':', '.').split()[0]
        path = f"{message.from_user.id}_{str(utc_now).replace(' ', '_').replace(':', '.')}"
        is_photo = 0
    else:
        path = food_irl.replace(chr(92), '/').split('/')[-1].split('.')[:-1]
        path = '.'.join(path)
        date = path.split('_')[1]
        is_photo = 1
    data_vis = await styling(answer, food_irl, path)
    if type(data_vis) == str:
        try:
            await load_msg.delete()
        except Exception as e:
            logger.warning("Не удалось удалить загрузочное сообщение: %s", e)
        await message.answer(
            "На отправленном вами фото не было обнаружено еды, пожалуста отправьте другое",
            reply_markup=kbi.main())
        return
    id = await add_food_to_table(data_vis[0], message.from_user.id, data_vis[1], data_vis[2], date, is_photo)

    await update_last_food_time(message.from_user.id)
    await state.update_data(food_id=id)

    data = await food_check_daily(message.from_user.id)
    goals = data[1]
    kcal_goal = int(goals[1])
    p_goal = float(goals[2].replace(",", "."))
    f_goal = float(goals[3].replace(",", "."))
    c_goal = float(goals[4].replace(",", "."))

    kcal_sum = 0
    for food_info in data[0]:
        kcal_sum += int(float(food_info[3].replace(",", ".")))

    kcal_sum = 0
    protein_sum = 0
    fat_sum = 0
    carbohydrate_sum = 0
    for food_info in data[0]:
        kcal_sum += int(float(food_info[3].replace(",", ".")))
        protein_sum += float(food_info[5].replace(",", "."))
        fat_sum += float(food_info[6].replace(",", "."))
        carbohydrate_sum += float(food_info[7].replace(",", "."))

    protein_sum = round(protein_sum, 2)
    fat_sum = round(fat_sum, 2)
    carbohydrate_sum = round(carbohydrate_sum, 2)

    if kcal_sum >= kcal_goal:
        mess = SEND_TABLE_MESSAGES[1].format(kcal_goal, kcal_sum, protein_sum, p_goal, fat_sum, f_goal, carbohydrate_sum, c_goal)
    else:
        mess = SEND_TABLE_MESSAGES[0].format(kcal_goal, kcal_sum, protein_sum, p_goal, fat_sum, f_goal, carbohydrate_sum, c_goal, kcal_goal - kcal_sum)

    try:
        await load_msg.delete()
    except Exception as e:
        logger.warning("Не удалось удалить загрузочное сообщение: %s", e)

    await message.answer_photo(types.FSInputFile(path=data_vis[2]))
    await message.answer(mess, reply_markup=kbi.add_food(id))
    
    # Логирование успешного добавления приёма пищи
    try:
        with open("meal_logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"Time: {datetime.datetime.now().isoformat()}\n")
            log_file.write(f"GPT Answer (Markdown Table):\n{answer}\n")
            log_file.write(f"Изображение: {food_irl if food_irl != '' else 'Нет изображения'}\n")
            log_file.write("-" * 40 + "\n")
    except Exception as log_e:
        logger.warning("Ошибка логирования: %s", log_e)

    return data_vis[0], data_vis[1], data_vis[2]

    # user_data = await get_user_info(message.from_user.id)

    # if user_data[10] is not None:
    #     await bot.send_message(user_data[10], f'<a href="tg://user?id={user_data[1]}">Клиент</a> сделал запись о приеме пищи', reply_markup=kbi.main(), parse_mode='HTML')
    #     await bot.send_photo(user_data[10], types.FSInputFile(path=data_vis[2]))

    #     await bot.send_message(user_data[10], mess, reply_markup=kbi.main())


@router.callback_query(F.data == "retry_send_food")
async def retry_send_food(callback: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    if data['ty'] == 'photo':
        # Если тип сообщения - фото, повторно вызываем обработчик для фото
        await add_food_photo(data['message'], state, bot)
    elif data['ty'] == 'voice':
        # Если тип сообщения - голосовое сообщение, повторно вызываем обработчик для голоса
        await add_food_voice(data['message'], state, bot)
    elif data['ty'] == 'text':
        # Если тип сообщения - текст, повторно вызываем обработчик для текста
        await add_food_text(data['message'], state, bot)



async def add_food(message: Message, answer, load_msg: Message, bot: Bot, state: FSMContext, food_irl = ''):
    if "НЕТ" in answer:
        # Логирование случая, когда еда не обнаружена
        try:
            with open("meal_logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"Time: {datetime.datetime.now().isoformat()}\n")
                log_file.write(f"Приём пищи не распознан. GPT Answer:\n{answer}\n")
                log_file.write("-" * 40 + "\n")
        except Exception as log_e:
            logger.error(f"Ошибка логирования: {log_e}")
        logger.info(answer)
        try:
            await load_msg.delete()
        except:
            logger.warning("Не удалось удалить загрузочное сообщение")
        await message.answer(
            "На отправленном вами фото не было обнаружено еды, пожалуста отправьте другое",
            reply_markup=kbi.main())
    else:
        try:
            await create_table(message, answer, load_msg, state, bot, food_irl)
        except Exception as e:
            # Логирование ошибки при добавлении еды
            try:
                with open("meal_logs.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"Time: {datetime.datetime.now().isoformat()}\n")
                    log_file.write(f"Ошибка при добавлении еды: {e}\n")
                    log_file.write("traceback: \n")
                    log_file.write(traceback.format_exc())
                    log_file.write("-" * 40 + "\n")
            except Exception as log_e:
                print(f"Ошибка логирования: {log_e}")
            await message.answer(
                "При распознавании произошла ошибка, попробуйте ещё раз",
                reply_markup=kbi.main())
            logger.error("Не удалось добавить еду: %s", e)


@all_router.message(F.photo)
async def add_food_photo(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.media_group_id:
        await message.answer("Пожалуйста, отправляй только одно фото за раз")
    else:
        photo = message.photo[-1]
        file_id = photo.file_id
        utc_now = datetime.datetime.now(pytz.utc)

        file = await bot.get_file(file_id)
        file_path = file.file_path

        # Create downloads/img directory if it doesn't exist
        downloads_img_dir = os.path.join("downloads", "img")
        os.makedirs(downloads_img_dir, exist_ok=True)
        
        # Prepare filename for downloaded image
        download_filename = f"{message.from_user.id}_{str(utc_now).replace(' ', '_').replace(':', '.')}.jpg"
        download_path = os.path.join(downloads_img_dir, download_filename)
        
        # Download a copy of the image to downloads/img folder
        await bot.download_file(file_path, download_path)

        # Create a cropped version of the image
        cropped_dir = os.path.join("downloads", "img", "croped")
        os.makedirs(cropped_dir, exist_ok=True)
        
        # Use the same filename for the cropped image
        cropped_path = os.path.join(cropped_dir, download_filename)
        
        # Copy the original image to the cropped directory
        import shutil
        shutil.copy2(download_path, cropped_path)
        

        load_msg = await message.answer('Фото загружено! Считаю ⏱', reply_markup=types.ReplyKeyboardRemove())

        with open(download_path, 'rb') as photo_file:
            photo_data = base64.b64encode(photo_file.read()).decode('utf-8')
        food_table = await vm.scan_food(f'data:image/jpeg;base64,{photo_data}')
        try:
            await add_food(message, food_table, load_msg, bot, state, cropped_path)
        except Exception as e:
            logger.error("Не удалось добавить еду: %s", e)
            await message.answer(
                "При распознавании произошла ошибка, попробуйте ещё раз",
                reply_markup=kbi.main())


@all_router.message(F.voice)
async def add_food_voice(message: Message, state: FSMContext, bot: Bot) -> None:
    load_msg = await message.answer('Считаю ⏱', reply_markup=types.ReplyKeyboardRemove())

    file_id = message.voice.file_id

    file = await message.bot.get_file(file_id)

    file_path = file.file_path
    file_name = f"{file_id}.ogg"
    destination = os.path.join("downloads", file_name)

    await message.bot.download_file(file_path, destination)

    text = await voice2text(destination)

    os.remove(destination)

    await message.answer(text, reply_markup=kbr.main())
    
    try:
        answer = await vm.text_to_food_table(text)
        await add_food(message, answer, load_msg, bot, state)
    except:
        answer = await vm.text_to_food_table(text)
        await add_food(message, answer, load_msg, bot, state)


@router.message(main_menu.add_food, F.text)
async def add_food_text(message: Message, state: FSMContext, bot: Bot) -> None:
    load_msg = await message.answer('Считаю ⏱', reply_markup=types.ReplyKeyboardRemove())

    text = message.text
    
    try:
        answer = await vm.text_to_food_table(text)
        await add_food(message, answer, load_msg, bot, state)
    except:
        answer = await vm.text_to_food_table(text)
        await add_food(message, answer, load_msg, bot, state)