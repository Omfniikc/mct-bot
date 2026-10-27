from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import StateFilter

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from middlewares.is_group import PrivateChatMiddleware
from generate.create_table import styling
from db_methods.user_methods import get_trainers_user_statistic, delete_user_from_trainer, get_trainer_user, get_all_measurements, get_all_subscription
from db_methods.goals_methods import update_goals, get_user_goal
from db_methods.food_methods import food_check_daily, get_dishes
from generate.create_table import create_trainer_table
from db_methods.user_methods import get_measurements_power, get_measurements_figure
from db_methods.progres import get_all_weight
from keyboards import inline as kbi
from keyboards import reply as kbr
from fsm.states import *
from text.messages import *
from text.lists import *
from config import *

import os
from datetime import datetime

router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.callback_query(F.data == "add_client")
async def add_client_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    message = callback.message
    user_id = callback.from_user.id
    bott = await bot.get_me()
    referral_link = f"https://t.me/{bott.username}?start={user_id}"
    await message.answer(
        f"Твоя ссылка: <code>{referral_link}</code>\n\nСкопируй и отправь её. Клиенты, перешедшие по ней будут привязаны к тебе!",
        parse_mode="HTML", reply_markup=kbi.main())



@router.callback_query(trainer_panel.measurements_figure)
async def figure(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    data = await get_measurements_figure(user_id, callback.data)

    if callback.data == "biceps":
        await state.update_data(figure="biceps")
        await get_measurements_figure_handler(callback, state, data)
    elif callback.data == "waist":
        await state.update_data(figure="waist")
        await get_measurements_figure_handler(callback, state, data)
    elif callback.data == "shoulder":
        await state.update_data(figure="shoulder")
        await get_measurements_figure_handler(callback, state, data)
        
    elif callback.data == "hips":
        await state.update_data(figure="hips")
        await get_measurements_figure_handler(callback, state, data)
        
    elif callback.data == "forearm":
        await state.update_data(figure="forearm")
        await get_measurements_figure_handler(callback, state, data)
        
    elif callback.data == "back":
        await state.update_data(figure="back")
        await get_measurements_figure_handler(callback, state, data)
        
    elif callback.data == "chest":
        await state.update_data(figure="chest")
        await get_measurements_figure_handler(callback, state, data)


@router.callback_query(StateFilter(trainer_panel), F.data == "back")
async def trainer_menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    await trainer_menu_handler(message, state)

@router.message(F.text == "Меню управления тренера")
async def trainer_menu_handler(message: Message, state: FSMContext):
    await message.answer("Выберите действие", reply_markup=kbr.trainer_menu())
    await state.set_state(trainer_panel.main_menu)


@router.message(trainer_panel.main_menu, F.text == "Статистика по всем клиентам")
async def all_user_statistic(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(trainer_panel.users_statistic)
    users_data = await get_trainers_user_statistic(message.from_user.id)
    print(users_data)
    if users_data:
        users = []
        for i in users_data:
            name = str(i[9])
            calories = str(i[1]) + "/"+ str(i[1+4])
            protein = str(i[2]) + "/"+ str(i[2+4])
            fat = str(i[3]) + "/"+ str(i[3+4])
            carbohydrate = str(i[4]) + "/"+ str(i[4+4])
            user = {"name": name, "kcal": calories, "p": protein, "f": fat, "c": carbohydrate}
            users.append(user)
        table_path = await create_trainer_table(users, message.from_user.id)
        await message.answer_photo(FSInputFile(path=table_path), caption="Статистика за сегодня", reply_markup=kbi.choose_day())
    else:
        await message.answer("У вас нет клиентов, вы можете добавить их вот здесь", reply_markup=kbi.add_client())

@router.callback_query(trainer_panel.users_statistic)
async def set_day_to_users_statistic(callback: CallbackQuery, state: FSMContext, bot: Bot):
    message = callback.message
    if callback.data in ("yesterday", "today"):
        day = -1 if callback.data == "yesterday" else 0
        mess = "Статистика за вчера" if callback.data == "yesterday" else "Статистика за сегодня"
        await state.set_state(trainer_panel.users_statistic)
        users_data = await get_trainers_user_statistic(callback.from_user.id, day)
        users = []
        for i in users_data:
            user = await bot.get_chat(i[0])
            name = str(user.first_name) + " " + str(user.last_name if user.last_name else "")
            calories = str(i[1]) + "/" + str(i[1 + 4])
            protein = str(i[2]) + "/" + str(i[2 + 4])
            fat = str(i[3]) + "/" + str(i[3 + 4])
            carbohydrate = str(i[4]) + "/" + str(i[4 + 4])
            user = {"name": name, "kcal": calories, "p": protein, "f": fat, "c": carbohydrate}
            users.append(user)
        table_path = await create_trainer_table(users, message.from_user.id)
        await message.answer_photo(FSInputFile(path=table_path), caption=mess, reply_markup=kbi.choose_day())
        return
    elif callback.data == "choose_my_date":
        await message.answer("Введи дату в формате дд.мм.гггг для отображения статистики за этот день", reply_markup=kbi.back())
        await state.set_state(trainer_panel.set_date_users)
        return

@router.message(trainer_panel.set_date_users)
async def set_date_users_stat(message: Message, state: FSMContext, bot: Bot):
    try:
        # Проверка формата
        date = datetime.strptime(message.text, '%d.%m.%Y')

        # Проверка даты не раньше 29.11.2024
        min_date = datetime(2024, 11, 29)

        if date < min_date:
            await message.answer("Дата не может быть раньше 29.11.2024, введите заново", reply_markup=kbi.back())
            return

        date_ls = message.text.split(".")
        date = f"{date_ls[2]}-{date_ls[1]}-{date_ls[0]}"
        await state.set_state(trainer_panel.users_statistic)
        users_data = await get_trainers_user_statistic(message.from_user.id, date=date)
        users = []
        for i in users_data:
            user = await bot.get_chat(i[0])
            name = str(user.first_name) + " " + str(user.last_name if user.last_name else "")
            calories = str(i[1]) + "/" + str(i[1 + 4])
            protein = str(i[2]) + "/" + str(i[2 + 4])
            fat = str(i[3]) + "/" + str(i[3 + 4])
            carbohydrate = str(i[4]) + "/" + str(i[4 + 4])
            user = {"name": name, "kcal": calories, "p": protein, "f": fat, "c": carbohydrate}
            users.append(user)
        table_path = await create_trainer_table(users, message.from_user.id)
        await message.answer_photo(FSInputFile(path=table_path), caption=f"Статистика за {message.text}",
                                   reply_markup=kbi.choose_day())
    except ValueError:
        await message.answer("Дата введена в неверном формате, введите в корректном формате дд.мм.гггг", reply_markup=kbi.back())
        return


@router.message(trainer_panel.main_menu, F.text == "Статистика по клиенту")
async def choose_user_statistic(message: Message, state: FSMContext, bot: Bot):
    users = await get_trainer_user(message.from_user.id)
    if not users:
        await message.answer("У вас нет клиентов, вы можете добавить их вот здесь", reply_markup=kbi.add_client())
        return
    await message.answer("Выберите что посмотреть", reply_markup=kbi.choose_users_statistic())
    await state.set_state(trainer_panel.choose_user_statistic)
    

@router.callback_query(trainer_panel.choose_user_statistic, F.data == "choose_user_food")
async def choose_user_statistic_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    users = await get_trainer_user(callback.from_user.id)
    await state.update_data(users_list=users)
    users_o = {}
    for user in users:
        user_id = user[0]
        user_name = user[1] + " " + user[2]
        users_o[user_name] = user_id
    await callback.message.answer("Выберите клиента", reply_markup=kbi.choose_users(users_o))
    await state.set_state(trainer_panel.choose_user_food)

@router.callback_query(trainer_panel.choose_user_statistic, F.data == "choose_user_measurements")
async def choose_user_statistic_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    users = await get_trainer_user(callback.from_user.id)
    await state.update_data(users_list=users)
    users_o = {}
    for user in users:
        user_id = user[0]
        user_name = user[1] + " " + user[2]
        users_o[user_name] = user_id
    await callback.message.answer("Выберите клиента", reply_markup=kbi.choose_users(users_o))
    await state.set_state(trainer_panel.choose_user_measurements)

@router.callback_query(trainer_panel.choose_user_food)
async def user_statistic(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    user = callback.data.split("_")[1]
    await state.set_state(trainer_panel.set_day_user)
    await state.update_data(user_id=user)
    data = await food_check_daily(user)
    food_daily = data[0]
    goals_data = data[1]
    if not food_daily:
        await message.answer(
            'Клиент сегодня ещё не добавлял приёмы пищи',
            reply_markup=kbi.choose_day())
    else:
        kcal_sum = 0
        protein_sum = 0
        fat_sum = 0
        carbohydrate_sum = 0
        weight_sum = 0
        all_dishes = []
        for food_info in food_daily:
            a = await get_dishes(food_info[0])
            a = list(map(lambda x: x[0], a))
            all_dishes.append(a)
            weight_sum += int(float(food_info[8]))
            kcal_sum += int(float(food_info[3]))
            protein_sum += float(food_info[5])
            fat_sum += float(food_info[6])
            carbohydrate_sum += float(food_info[7])
        await message.answer(
            f"Статистика на {food_daily[0][4]}\n\n" +
            f"Дневная цель: {goals_data[1]} ккал.\n" +
            f"Сегодня вы съели {kcal_sum} ккал. 🔥\n\n" +
            f"Белки: {round(protein_sum, 1)} г/ {goals_data[2]} г 💪\n" +
            f"Жиры: {round(fat_sum, 1)} г/ {goals_data[3]} г 🧈\n" +
            f"Углеводы: {round(carbohydrate_sum, 1)} г/ {goals_data[4]} г 🍞",
            reply_markup=kbr.main()
        )
        food = [
            '| Название | Вес, г | Ккал | Б, г | Ж, г | У, г |\n|-------|--------|--------|--------|--------|--------|\n']
        i = 0
        for food_info in food_daily:
            with open(f'{food_info[2][:-3]}txt') as f:
                text = f.read()
            text = text.replace('ИТОГО', ' '.join(all_dishes[i]))
            text = text.split('\n')
            food.append(text[-1] + '\n')
            i += 1
        food.append(
            f'| ИТОГО    | {weight_sum}    | {kcal_sum}   | {round(protein_sum, 2)}  | {round(fat_sum, 2)}  | {round(carbohydrate_sum, 2)}   |')
        ans = ''.join(food)
        path = f"{message.from_user.id}_all_food"
        data_vis = await styling(markdown_table=ans, path=path)
        await message.answer_photo(FSInputFile(path=data_vis[2]), reply_markup=kbi.choose_day())
        os.remove(data_vis[2])
        os.remove(data_vis[2][:-3] + 'txt')

@router.callback_query(trainer_panel.choose_user_measurements)
async def user_measurements(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    user = callback.data.split("_")[1]
    await state.update_data(user_id=user)
    data = await state.get_data()
    users = data["users_list"]
    measurements_data = await get_all_measurements(user)
    measurements_figure = measurements_data["figure"]
    measurements_exercises = measurements_data["exercises"]
    n = measurements_figure.get("biceps", {}).get("value", 0)
    waist = measurements_figure.get("waist", {}).get("value", 0)
    shoulder = measurements_figure.get("shoulder", {}).get("value", 0)
    hips = measurements_figure.get("hips", {}).get("value", 0)
    forearm = measurements_figure.get("forearm", {}).get("value", 0)
    back = measurements_figure.get("back", {}).get("value", 0)
    chest = measurements_figure.get("chest", {}).get("value", 0)

    bench_press = measurements_exercises.get("bench_press", {}).get("weight", 0)
    bench_press_count = measurements_exercises.get("bench_press", {}).get("count", 0)
    pull_ups = measurements_exercises.get("push_ups", {}).get("weight", 0)
    pull_ups_count = measurements_exercises.get("push_ups", {}).get("count", 0)
    dips = measurements_exercises.get("dips", {}).get("weight", 0)
    dips_count = measurements_exercises.get("dips", {}).get("count", 0)
    dumbbell_flyes = measurements_exercises.get("dumbbell_flyes", {}).get("weight", 0)
    dumbbell_flyes_count = measurements_exercises.get("dumbbell_flyes", {}).get("count", 0)
    delta_pull = measurements_exercises.get("delta_pull", {}).get("weight", 0)
    delta_pull_count = measurements_exercises.get("delta_pull", {}).get("count", 0)
    barbell_curl = measurements_exercises.get("barbell_curl", {}).get("weight", 0)
    barbell_curl_count = measurements_exercises.get("barbell_curl", {}).get("count", 0)
    barbell_squat = measurements_exercises.get("barbell_squat", {}).get("weight", 0)
    barbell_squat_count = measurements_exercises.get("barbell_squat", {}).get("count", 0)
    deadlift = measurements_exercises.get("deadlift", {}).get("weight", 0)
    deadlift_count = measurements_exercises.get("deadlift", {}).get("count", 0)
    dumbbell_overhead_press = measurements_exercises.get("dumbbell_overhead_press", {}).get("weight", 0)
    dumbbell_overhead_press_count = measurements_exercises.get("dumbbell_overhead_press", {}).get("count", 0)
    barbell_overhead_press = measurements_exercises.get("barbell_overhead_press", {}).get("weight", 0)
    barbell_overhead_press_count = measurements_exercises.get("barbell_overhead_press", {}).get("count", 0)

    
    print(measurements_data)
    for i in users:
        if i[0] == user:
            k = i


    await message.answer(f"Данные клиента {k[1] + " " + k[2]} сейчас")
    await message.answer(
        f'''
Фигура
Бицепс: {n} см
Талия: {waist} см
Обхват плеч: {shoulder} см
Обхват бёдер: {hips} см
Предплечье: {forearm} см
Икры: {back} см
Обхват грудных: {chest} см

Силовые
Жим лёжа: {bench_press}/{bench_press_count}
Подтягивания: {pull_ups}/{pull_ups_count}
Брусья: {dips}/{dips_count}
Махи с гантелями: {dumbbell_flyes}/{dumbbell_flyes_count}
Протяжка на дельты: {delta_pull}/{delta_pull_count}
Штанга на бицепс: {barbell_curl}/{barbell_curl_count}
Присед со штангой: {barbell_squat}/{barbell_squat_count}
Становая тяга: {deadlift}/{deadlift_count}
Жим гантелей на вертикальной скамье: {dumbbell_overhead_press}/{dumbbell_overhead_press_count}
Жим штанги на вертикальной скамье: {barbell_overhead_press}/{barbell_overhead_press_count}
'''
    )
    await state.set_state(trainer_panel.user_measurements_stat)
    await message.answer("Посмотреть прогресс по определеным замерам", reply_markup=kbi.measurements_users())

@router.callback_query(trainer_panel.user_measurements_stat, F.data == "yes")
async def measurements_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Какие данные хотите посмотреть?", reply_markup=kbr.measurements())
    await state.set_state(trainer_panel.choose_user_measurements_stat)

@router.message(trainer_panel.choose_user_measurements_stat)
async def q(message: Message, state: FSMContext):

    if message.text == "Вес":
        await view_weight_statistics_handler(message, state)
        await state.set_state(trainer_panel.measurements_weight)
    elif message.text == "Фигура":
        await message.answer("Выбери что замеряем", reply_markup=kbi.figure())
        await state.set_state(trainer_panel.measurements_figure)
        print(state.get_state)
    elif message.text == "Силовые":
        await message.answer("Выбери что замеряем", reply_markup=kbi.power())
        await state.set_state(trainer_panel.measurements_power)


@router.callback_query(trainer_panel.measurements_power)
async def power(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    data = await get_measurements_power(user_id, callback.data)


    if callback.data == "push_ups": 
        await state.update_data(power="push_ups")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "dips":
        await state.update_data(power="dips")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "bench_press":
        await state.update_data(power="bench_press")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "dumbbell_flyes":
        await state.update_data(power="dumbbell_flyes")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "delta_pull":
        await state.update_data(power="delta_pull")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "barbell_curl":
        await state.update_data(power="barbell_curl")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "barbell_squat":
        await state.update_data(power="barbell_squat")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "deadlift":
        await state.update_data(power="deadlift")
        await get_measurements_power_handler(callback, state, data)
    elif callback.data == "dumbbell_overhead_press":
        await state.update_data(power="dumbbell_overhead_press")
        await get_measurements_power_handler(callback, state, data)  
    elif callback.data == "barbell_overhead_press":
        await state.update_data(power="barbell_overhead_press")
        await get_measurements_power_handler(callback, state, data)

async def get_measurements_power_handler(callback: CallbackQuery, state: FSMContext, data: list):
    data_s = await state.get_data()
    await callback.message.answer(f"Вот твои замеры по {MEASUREMENTS[data_s['power']]}")
    if not data:
        text = "У вас пока нет замеров"
    else:
        text = ""
        for i in data:
            s = f"{i[2]} - {i[3]}/{i[4]}\n\n"
            text += s

    await callback.message.answer(text, reply_markup=kbi.back_main())
    await state.set_state(trainer_panel.measurements_power)


async def get_measurements_figure_handler(callback: CallbackQuery, state: FSMContext, data: list):
    data_s = await state.get_data()
    await callback.message.answer(f"Вот твои замеры по {MEASUREMENTS[data_s['figure']]}")
    if not data:
        text = "У вас пока нет замеров"
    else:
        text = ""
        for i in data:
            s = f"{i[2]} - {i[3]}\n\n"
            text += s

    await callback.message.answer(text, reply_markup=kbi.back_main())
    await state.set_state(trainer_panel.measurements_figure_l)

async def view_weight_statistics_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    data = await get_all_weight(user_id)
    await message.answer("Статистика по весу:")
    if not data:
        text = "У вас пока нет замеров"
    else:
        text = ""
        for i in data:
            s = f"{i[2]} - {i[3]}\n\n"
            text += s

    await message.answer(text, reply_markup=kbi.back_main())

@router.callback_query(trainer_panel.set_day_user)
async def set_day_to_user_statistic(callback: CallbackQuery, state: FSMContext, bot: Bot):
    message = callback.message
    data = await state.get_data()
    if callback.data in ("yesterday", "today"):
        day = -1 if callback.data == "yesterday" else 0
        mess = "Статистика за вчера" if callback.data == "yesterday" else "Статистика за сегодня"
        await state.set_state(trainer_panel.set_day_user)
        user_data = await food_check_daily(user_id=data["user_id"], days=day)
        food_daily = user_data[0]
        goals_data = user_data[1]
        if not food_daily:
            await message.answer(
                'Клиент сегодня ещё не добавлял приёмы пищи',
                reply_markup=kbi.choose_day())
        else:
            kcal_sum = 0
            protein_sum = 0
            fat_sum = 0
            carbohydrate_sum = 0
            weight_sum = 0
            all_dishes = []
            for food_info in food_daily:
                a = await get_dishes(food_info[0])
                a = list(map(lambda x: x[0], a))
                all_dishes.append(a)
                weight_sum += int(float(food_info[8]))
                kcal_sum += int(float(food_info[3]))
                protein_sum += float(food_info[5])
                fat_sum += float(food_info[6])
                carbohydrate_sum += float(food_info[7])
            await message.answer(
                f"Статистика на {food_daily[0][4]}\n\n" +
                f"Дневная цель: {goals_data[1]} ккал.\n" +
                f"Сегодня вы съели {kcal_sum} ккал. 🔥\n\n" +
                f"Белки: {round(protein_sum, 1)} г/ {goals_data[2]} г 💪\n" +
                f"Жиры: {round(fat_sum, 1)} г/ {goals_data[3]} г 🧈\n" +
                f"Углеводы: {round(carbohydrate_sum, 1)} г/ {goals_data[4]} г 🍞",
                reply_markup=kbr.main()
            )
            food = [
                '| Название | Вес, г | Ккал | Б, г | Ж, г | У, г |\n|-------|--------|--------|--------|--------|--------|\n']
            i = 0
            for food_info in food_daily:
                with open(f'{food_info[2][:-3]}txt') as f:
                    text = f.read()
                text = text.replace('ИТОГО', ' '.join(all_dishes[i]))
                text = text.split('\n')
                food.append(text[-1] + '\n')
                i += 1
            food.append(
                f'| ИТОГО    | {weight_sum}    | {kcal_sum}   | {round(protein_sum, 2)}  | {round(fat_sum, 2)}  | {round(carbohydrate_sum, 2)}   |')
            ans = ''.join(food)
            path = f"{message.from_user.id}_all_food"
            data_vis = await styling(ans, path, 0)
            await message.answer_photo(FSInputFile(path=data_vis[2]), caption=mess, reply_markup=kbi.choose_day())
            os.remove(data_vis[2])
            os.remove(data_vis[2][:-3] + 'txt')
    elif callback.data == "choose_my_date":
        await message.answer("Введи дату в формате дд.мм.гггг для отображения статистики за этот день", reply_markup=kbi.back())
        await state.set_state(trainer_panel.set_date_user)
        return

@router.message(trainer_panel.set_date_user)
async def set_date_users_stat(message: Message, state: FSMContext, bot: Bot):
    try:
        # Проверка формата
        date = datetime.strptime(message.text, '%d.%m.%Y')

        # Проверка даты не раньше 29.11.2024
        min_date = datetime(2024, 11, 29)

        if date < min_date:
            await message.answer("Дата не может быть раньше 29.11.2024, введите заново", reply_markup=kbi.back())
            return

        date_ls = message.text.split(".")
        date = f"{date_ls[2]}-{date_ls[1]}-{date_ls[0]}"
        await state.set_state(trainer_panel.choose_user_statistic)
        user_data = await food_check_daily(message.from_user.id, date=date)
        food_daily = user_data[0]
        goals_data = user_data[1]
        if not food_daily:
            await message.answer(
                'Клиент сегодня ещё не добавлял приёмы пищи',
                reply_markup=kbi.choose_day())
        else:
            kcal_sum = 0
            protein_sum = 0
            fat_sum = 0
            carbohydrate_sum = 0
            weight_sum = 0
            all_dishes = []
            for food_info in food_daily:
                a = await get_dishes(food_info[0])
                a = list(map(lambda x: x[0], a))
                all_dishes.append(a)
                weight_sum += int(float(food_info[8]))
                kcal_sum += int(float(food_info[3]))
                protein_sum += float(food_info[5])
                fat_sum += float(food_info[6])
                carbohydrate_sum += float(food_info[7])
            await message.answer(
                f"Статистика на {food_daily[0][4]}\n\n" +
                f"Дневная цель: {goals_data[1]} ккал.\n" +
                f"Сегодня вы съели {kcal_sum} ккал. 🔥\n\n" +
                f"Белки: {round(protein_sum, 1)} г/ {goals_data[2]} г 💪\n" +
                f"Жиры: {round(fat_sum, 1)} г/ {goals_data[3]} г 🧈\n" +
                f"Углеводы: {round(carbohydrate_sum, 1)} г/ {goals_data[4]} г 🍞",
                reply_markup=kbr.main()
            )
            food = [
                '| Название | Вес, г | Ккал | Б, г | Ж, г | У, г |\n|-------|--------|--------|--------|--------|--------|\n']
            i = 0
            for food_info in food_daily:
                with open(f'{food_info[2][:-3]}txt') as f:
                    text = f.read()
                text = text.replace('ИТОГО', ' '.join(all_dishes[i]))
                text = text.split('\n')
                food.append(text[-1] + '\n')
                i += 1
            food.append(
                f'| ИТОГО    | {weight_sum}    | {kcal_sum}   | {round(protein_sum, 2)}  | {round(fat_sum, 2)}  | {round(carbohydrate_sum, 2)}   |')
            ans = ''.join(food)
            path = f"{message.from_user.id}_all_food"
            data_vis = await styling(ans, path, 0)
            await message.answer_photo(FSInputFile(path=data_vis[2]), caption=f"Статистика за {message.text}", reply_markup=kbi.choose_day())
            os.remove(data_vis[2])
            os.remove(data_vis[2][:-3] + 'txt')
    except ValueError:
        await message.answer("Дата введена в неверном формате, введите в корректном формате дд.мм.гггг", reply_markup=kbi.back())
        return


@router.message(trainer_panel.main_menu, F.text == "Задать цели для клиента")
async def choose_set_goals_user(message: Message, state: FSMContext, bot: Bot):
    users = await get_trainer_user(message.from_user.id)
    mess = "У вас нет клиентов, вы можете добавить их вот здесь" if not users else "Выберите клиента"
    if users is not None:
        users_o = {}
        for user in users:
            user_id = user[0]
            user_name = user[1] + " " + user[2]
            users_o[user_name] = user_id

    keyboard = kbi.add_client() if not users else kbi.choose_users(users_o)
    await message.answer(mess, reply_markup=keyboard)
    await state.set_state(trainer_panel.main_menu if not users else trainer_panel.user_goals)

@router.callback_query(trainer_panel.user_goals)
async def set_goals_user(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    user = callback.data.split("_")[1]
    await state.update_data(user_id=user)
    user_data = await get_user_goal(user)
    await message.answer(
        "Сейчас у клиента задано {cal} калорий, {protein} белков, {fat} жиров, {carbs} углеводов".format(
            cal=user_data[1], protein=user_data[2], fat=user_data[3], carbs=user_data[4]), reply_markup=kbi.back())
    await message.answer("Чтобы задать цели по КБЖУ для клиента укажите количество белков, жиров и углеводов клиенту необходимо потреблять, и бот засчитает цель по калориям.")
    await message.answer("1) Введите цель по белкам (только число):")
    await state.set_state(trainer_panel.goal_protein)

@router.message(trainer_panel.goal_protein)
async def set_protein(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await state.update_data(protein=int(message.text))
        await message.answer("2) Введите цель по жирам (только число):")
        await state.set_state(trainer_panel.goal_fat)

@router.message(trainer_panel.goal_fat)
async def set_fat(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await state.update_data(fat=int(message.text))
        await message.answer("3) Введите цель по углеводам (только число):")
        await state.set_state(trainer_panel.goal_carbohydrate)

@router.message(trainer_panel.goal_carbohydrate)
async def set_carbohydrate(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await state.update_data(carbohydrate=int(message.text))
        data = await state.get_data()
        cal = data["protein"]*4+data["fat"]*9+data["carbohydrate"]*4
        await state.update_data(cal=cal)
        await message.answer('''4) Исходя из расчета калорий по формуле 
Белки * 4 + жиры * 9 + углеводы * 4 = ккал.
    
Вашему клиенту необходимо потреблять {kcal} калорий каждый день.'''.format(kcal=cal), reply_markup=kbi.save_cal())
        await state.set_state(trainer_panel.goal_kcal)

@router.callback_query(trainer_panel.goal_kcal)
async def set_cal(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    data = await state.get_data()
    if callback.data == "save":
        await update_goals(data["user_id"], kcal=data["cal"], protein=data["protein"], fat=data["fat"], carbohydrate=data["carbohydrate"])
        await state.set_state(trainer_panel.main_menu)
        user_data = await get_user_goal(data["user_id"])
        await message.answer(
            "Теперь у клиента задано {cal} калорий, {protein} белков, {fat} жиров, {carbs} углеводов".format(
                cal=user_data[1], protein=user_data[2], fat=user_data[3], carbs=user_data[4]), reply_markup=kbi.back())

    elif callback.data == "set":
        await message.answer("Введи необходимое количество калорий")
        await state.set_state(trainer_panel.goal_kcal)

@router.message(trainer_panel.goal_kcal)
async def set_cal_r(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await state.update_data(cal=message.text)
        data = await state.get_data()
        await update_goals(data["user_id"], kcal=data["cal"], protein=data["protein"], fat=data["fat"], carbohydrate=data["carbohydrate"])

        await state.set_state(trainer_panel.main_menu)
        user_data = await get_user_goal(data["user_id"])
        await message.answer(
            "Теперь у клиента задано {cal} калорий, {protein} белков, {fat} жиров, {carbs} углеводов".format(
                cal=user_data[1], protein=user_data[2], fat=user_data[3], carbs=user_data[4]), reply_markup=kbi.back())


@router.message(trainer_panel.main_menu, F.text == "Добавить клиента")
async def user_management(message: Message, state: FSMContext, bot: Bot):
    user_id = message.chat.id
    bott = await bot.get_me()
    referral_link = f"https://t.me/{bott.username}?start={user_id}"
    await message.answer(
        f"Твоя ссылка: <code>{referral_link}</code>\n\nСкопируй и отправь её. Клиенты, перешедшие по ней будут привязаны к тебе!",
        parse_mode="HTML")
    users = await get_trainer_user(user_id)
    users = list(map(lambda x: x[0], users))
    mess = "У вас нет клиентов, вы можете добавить в сообщении выше" if not users else "Если хочешь удалить клиента, то выбери его из списка ниже"

    users_o = {}
    for user in users:
        user = await bot.get_chat(user)
        users_o[user.first_name] = user.id
    keyboard = kbi.main() if not users else kbi.choose_users(users_o)
    await message.answer(mess, reply_markup=keyboard)
    await state.set_state(trainer_panel.main_menu if not users else trainer_panel.delete_user)


@router.callback_query(trainer_panel.delete_user)
async def delete_user_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    message = callback.message
    user_id = callback.data.split("_")[1]
    user = await bot.get_chat(user_id)
    await state.update_data(user_id=user_id)
    await message.answer("Вы уверены что хотите удалить @{}".format(user.username), reply_markup=kbi.yes_no())
    await state.set_state(trainer_panel.delete_user_accept)

@router.callback_query(trainer_panel.delete_user_accept)
async def delete_user_accept_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    message = callback.message
    data = await state.get_data()
    if callback.data in ["yes", "no"]:
        if callback.data == "yes":
            print(1)
            await delete_user_from_trainer(data["user_id"])
            await message.answer("Клиент удален", reply_markup=kbi.main())
        elif callback.data == "no":
            await user_management(message, state, bot)

bot = Bot(token=TG_TOKEN)

async def my_task():
    trainers = await get_all_subscription()
    for user_id in list(map(lambda x: x[0], trainers)):
        users_data = await get_trainers_user_statistic(user_id)
        print(users_data)
        if users_data:
            users = []
            for i in users_data:
                name = str(i[9])
                calories = str(i[1]) + "/"+ str(i[1+4])
                protein = str(i[2]) + "/"+ str(i[2+4])
                fat = str(i[3]) + "/"+ str(i[3+4])
                carbohydrate = str(i[4]) + "/"+ str(i[4+4])
                user = {"name": name, "kcal": calories, "p": protein, "f": fat, "c": carbohydrate}
                users.append(user)
            table_path = await create_trainer_table(users, user_id)
            await bot.send_photo(user_id, FSInputFile(path=table_path), caption="Статистика за сегодня", reply_markup=kbi.main())
        else:
            await bot.send_message(user_id, "У вас нет клиентов, вы можете добавить их вот здесь", reply_markup=kbi.add_client())


scheduler = AsyncIOScheduler()
tz = timezone("Europe/Moscow")

async def trainers_stat():
    scheduler.add_job(my_task, CronTrigger(hour=21, minute=0, timezone=tz))

    scheduler.start()