from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import logging

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from config import *
from keyboards import inline as kbi
from db_methods.food_methods import get_last_food_time as get_users
from db_methods.user_methods import set_notification
from middlewares.is_group import PrivateChatMiddleware


bot = Bot(token=TG_TOKEN)
scheduler = AsyncIOScheduler()

router = Router()
router.message.middleware(PrivateChatMiddleware())

@router.callback_query(F.data == "notify_true_cancel")
async def cancel_notify(callback: CallbackQuery):
    await set_notification(callback.from_user.id, 0)
    await callback.message.edit_text("Напоминания отключены", reply_markup=kbi.main())


@router.callback_query(F.data == 'notify_cancel')   
async def set_time(callback: CallbackQuery, state: FSMContext):
    msg = callback.message
    await state.update_data(notify_msg=msg)
    await callback.message.edit_text(
        "Ты точно хочешь отменить напоминания?\n"+
        "Пользователи, которые используют напоминания добиваются результатов на 460% быстрее",
        reply_markup=kbi.true_notify())

@router.callback_query(F.data == "not_cancel_notify")
async def not_cancel(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(text=data["notify_msg"].text, reply_markup=kbi.notification())


async def send_reminder(user_id, time):
    if time == 1:
        text = "Доброе утро! ☀️ Не забудь внести свой завтрак"
    elif time == 2:
        text = "Не забудь добавить обед ☁️"
    elif time == 3:
        text = "Пришло время добавить ужин 🌙"
    await bot.send_message(user_id, text=text, reply_markup=kbi.notification())
    if str(user_id) == str(ADMIN_ID):
        await bot.send_document(ADMIN_ID, FSInputFile(path="./main.db"), caption="бэкап базы данных")

async def task():
    users = await get_users()
    for user in users:
        if user[3] == "0":
            continue
        now = datetime.utcnow()
        try:
            # Попробуем сначала с дробными секундами
            date_time_obj = datetime.strptime(user[2].strip(), "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=2)
        except ValueError:
            try:
                # Если не получилось, попробуем без дробных секунд
                date_time_obj = datetime.strptime(user[2].strip(), "%Y-%m-%d %H:%M:%S") + timedelta(hours=2)
            except ValueError as e:
                # Логируем ошибку и пропускаем пользователя
                logging.error(f"Ошибка разбора даты для пользователя {user[1]}: {user[2]} - {e}")
                continue

        if now == now.replace(hour=(int(user[4]) % 24), minute=0) and date_time_obj < now:
            try:
                await send_reminder(int(user[1]), 1)
            except Exception as e:
                logging.error(f"Не удалось отправить напоминание (1): {e}")
        elif now == now.replace(hour=(int(user[5]) % 24), minute=0) and date_time_obj < now:
            try:
                await send_reminder(int(user[1]), 2)
            except Exception as e:
                logging.error(f"Не удалось отправить напоминание (2): {e}")
        elif now == now.replace(hour=(int(user[6]) % 24), minute=0) and date_time_obj < now:
            try:
                await send_reminder(int(user[1]), 3)
            except Exception as e:
                logging.error(f"Не удалось отправить напоминание (3): {e}")

async def start_scheduler_notify():
    scheduler.add_job(task, 'interval', minutes=1)
    scheduler.start()
