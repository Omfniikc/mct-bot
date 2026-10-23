from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

import os
from datetime import datetime, timedelta
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import traceback


from keyboards import reply as kbr
from keyboards import inline as kbi
from generate.create_table import styling
from db_methods.user_methods import get_all_subscription
from db_methods.food_methods import food_check_daily, get_dishes
from db_methods.goals_methods import get_user_goal
from middlewares.is_group import PrivateChatMiddleware
from middlewares.is_subscrioption import HasSubscriptionFilter
from gpt_models import scan_food as gen


from config import TG_TOKEN

router = Router()
router.message.middleware(PrivateChatMiddleware())
router.message.middleware(HasSubscriptionFilter())
bot = Bot(token=TG_TOKEN)
logger = logging.getLogger(__name__)


@router.message(F.text == 'Просмотр приемов пищи за день')
async def process_name(message: Message, state: FSMContext) -> None:
    data = await food_check_daily(message.from_user.id)
    food_daily = data[0]
    goals_data = data[1]
    if not food_daily:
        await message.answer(
            'Ты сегодня ещё не добавлял приёмы пищи 😒',
            reply_markup=kbr.main())
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
            f"Твоя статистика за сегодня {datetime.strftime(datetime.strptime(food_daily[0][4], "%Y-%m-%d"), "%d.%m.%y")} 🍽\n\n"+
            f"Дневная цель: {goals_data[1]} ккал.\n"+
            f"Сегодня вы съели {kcal_sum} ккал. 🔥\n\n"+
            f"Белки: {round(protein_sum, 1)} г/ {goals_data[2]} г 💪\n"+
            f"Жиры: {round(fat_sum, 1)} г/ {goals_data[3]} г 🧈\n"+
            f"Углеводы: {round(carbohydrate_sum, 1)} г/ {goals_data[4]} г 🍞",
            reply_markup=kbr.main()
        )
        food = ['| Название | Вес, г | Ккал | Б, г | Ж, г | У, г |\n|-------|--------|--------|--------|--------|--------|\n']
        i = 0
        for food_info in food_daily:
            
            try:
                with open(f'{os.path.splitext(food_info[2])[0]}.txt', encoding='utf-8') as f:
                    text = f.read()
            except FileNotFoundError:
                text = "File not found"
            text = text.replace('ИТОГО', ' '.join(all_dishes[i]))
            text = text.split('\n')
            food.append(text[-1] + '\n')
            i += 1
        food.append(f'| ИТОГО    | {weight_sum}    | {kcal_sum}   | {round(protein_sum, 2)}  | {round(fat_sum, 2)}  | {round(carbohydrate_sum, 2)}   |')
        ans = ''.join(food)
        path = f"{message.from_user.id}_all_food"
        data_vis = await styling(ans, path=path)
        await message.answer_photo(FSInputFile(path=data_vis[2]))
        os.remove(data_vis[2])
        os.remove(data_vis[2][:-3]+'txt')


@router.message(F.text == "Просмотр приемов пищи за неделю")
async def view_weekly_food(message: Message):
    user_id = message.from_user.id
    today = datetime.utcnow().date()
    food_weekly = []
    goals_data = await get_user_goal(user_id)

    all_weight_sum = 0
    all_kcal_sum = 0
    all_protein_sum = 0
    all_fat_sum = 0
    all_carbohydrate_sum = 0

    for i in range(7):
        day = today - timedelta(days=i)
        food_daily, _ = await food_check_daily(user_id, day)
        food_weekly.append((day, food_daily))

    food = ['| Название | Вес, г | Ккал | Б, г | Ж, г | У, г |\n|-------|--------|--------|--------|--------|--------|--------|\n']
    
    for day, food_daily in food_weekly:
        formatted_day = day.strftime("%d.%m.%y")
        if not food_daily:
            food.append(f'| {formatted_day} | 0 | 0 | 0 | 0 | 0 |\n')
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
            food.append(f'| {formatted_day} | {weight_sum} | {kcal_sum} | {round(protein_sum, 1)} | {round(fat_sum, 1)} | {round(carbohydrate_sum, 1)} |\n')
            all_weight_sum += weight_sum
            all_kcal_sum += kcal_sum
            all_protein_sum += protein_sum
            all_fat_sum += fat_sum
            all_carbohydrate_sum += carbohydrate_sum
    food.append(f'| ИТОГО    | {all_weight_sum}    | {all_kcal_sum}   | {round(all_protein_sum, 2)}  | {round(all_fat_sum, 2)}  | {round(all_carbohydrate_sum, 2)}   |')
    
    await message.answer(
            f"Ваша статистика за неделю\n\n"+
            f"Дневная цель: {goals_data[1]} ккал.\n"+
            f"В среднем вы съели {round(all_kcal_sum/7, 1)} ккал. 🔥\n\n"+
            f"Белки: {round(all_protein_sum/7, 1)} г/ {goals_data[2]} г 💪\n"+
            f"Жиры: {round(all_fat_sum/7, 1)} г/ {goals_data[3]} г 🧈\n"+
            f"Углеводы: {round(all_carbohydrate_sum/7, 1)} г/ {goals_data[4]} г 🍞",
            reply_markup=kbr.main()
        )

    ans = ''.join(food)
    path = f"{message.from_user.id}_weekly_food"
    data_vis = await styling(ans, path=path)
    
    await message.answer_photo(FSInputFile(path=data_vis[2]), reply_markup=kbi.main())
    os.remove(data_vis[2])
    os.remove(data_vis[2][:-3]+'txt')


@router.message(F.text == "Просмотр приемов пищи за месяц")
async def test_note(message: Message):
    await message.answer("Эта функция пока недоступна", reply_markup=kbr.main())


async def my_task():
    users = await get_all_subscription()
    for user in users:
        try:
            if int(user[1]) == 1:
                user_id = user[0]
                data = await food_check_daily(user_id)
                food_daily = data[0]
                goals_data = data[1]
                if not food_daily:
                    await bot.send_message(user_id,
                        'Ты сегодня ещё не добавлял приёмы пищи 😒',
                        reply_markup=kbr.main())
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
                    await bot.send_message(user_id,
                        f"Твоя статистика за сегодня {datetime.strftime(datetime.strptime(food_daily[0][4], "%Y-%m-%d"), "%d.%m.%y")} 🍽\n\n"+
                        f"Дневная цель: {goals_data[1]} ккал.\n"+
                        f"Сегодня вы съели {kcal_sum} ккал. 🔥\n\n"+
                        f"Белки: {round(protein_sum, 1)} г/ {goals_data[2]} г 💪\n"+
                        f"Жиры: {round(fat_sum, 1)} г/ {goals_data[3]} г 🧈\n"+
                        f"Углеводы: {round(carbohydrate_sum, 1)} г/ {goals_data[4]} г 🍞",
                        reply_markup=kbr.main()
                    )
                    food = ['| Название | Вес, г | Ккал | Б, г | Ж, г | У, г |\n|-------|--------|--------|--------|--------|--------|\n']
                    i = 0
                    for food_info in food_daily:
                        with open(f'{food_info[2][:-3]}txt', encoding='utf-8') as f:
                            text = f.read()
                        text = text.replace('ИТОГО', ' '.join(all_dishes[i]))
                        text = text.split('\n')
                        food.append(text[-1] + '\n')
                        i += 1
                    food.append(f'| ИТОГО    | {weight_sum}    | {kcal_sum}   | {round(protein_sum, 2)}  | {round(fat_sum, 2)}  | {round(carbohydrate_sum, 2)}   |')
                    ans = ''.join(food)
                    path = f"{user_id}_all_food"
                    data_vis = await styling(ans, path=path)
                    await bot.send_photo(user_id, FSInputFile(path=data_vis[2]))
                    
                    # Получаем совет по питанию, анализируя таблицу
                    advice = await gen.generate_nutrition_advice(ans)
                    await bot.send_message(user_id, f"🔔Совет по питанию от ИИ:\n{advice}", reply_markup=kbr.main())
                    
                    os.remove(data_vis[2])
                    os.remove(data_vis[2][:-3]+'txt')
        except Exception as e:
            logger.warning("Error processing user daily note %s: %s", user[0], e)
            
            with open("error_logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"Time: {datetime.now().isoformat()} - User: {user[0]} - Error: {e}\n")
                log_file.write("Traceback:\n")
                traceback.print_exc(file=log_file)


scheduler = AsyncIOScheduler()
tz = timezone("Europe/Moscow")

async def stat():
    scheduler.add_job(my_task, CronTrigger(hour=20, minute=0, timezone=tz))

    scheduler.start()