from aiogram import F, Router, Bot, types
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from requests.exceptions import HTTPError

from middlewares.is_group import PrivateChatMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from yookassa import Configuration, Payment
import uuid
import qrcode
import logging
from asyncio import to_thread
import asyncio
import time

from keyboards import reply as kbr
from keyboards import inline as kbi
from fsm.states import user_data
from db_methods.user_methods import (
    get_all_subscription,
    off_subscription,
    get_user_email,
    get_trainer_users, 
    add_subscription,
    save_user_payment,
    change_sub_not,
    save_user_consent,
    get_user_consent,
    get_user_payment,
    get_subscription
)

from text.messages import *
from config import *


bot = Bot(token=TG_TOKEN)
scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)

PRICES = {
    "MONTH_PRICE": {"description":'Подписка на месяц для тренера', "amount":"1290.00"},
    "THREE_MONTH_PRICE": {"description":'Подписка на 3 месяца для тренера', "amount":"2690.00"}
}

router = Router()
router.message.middleware(PrivateChatMiddleware())

Configuration.account_id = SHOP_ID
Configuration.secret_key = PAY_TOKEN

async def create_payment(data, email):
    n = await bot.get_me()
    idempotence_key = str(uuid.uuid4())
    try:
        payment = Payment.create({
            "amount": {
                "value": data["amount"],
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://t.me/{n.username}"
            },
            "capture": True,
            "description": f"{data['description']}, {email}",
            "receipt": {
                "customer": {
                    "email": email
                },
                "items": [
                    {
                        "description": data["description"],
                        "quantity": "1.00",
                        "amount": {
                            "value": data["amount"],
                            "currency": "RUB"
                        },
                        "vat_code": 1  # Код НДС (1 означает 20%)
                    }
                ]
            },
            "metadata": {
                "cms_name": "yookassa_sdk_python"
            },
            "save_payment_method" : True 
        }, idempotence_key)
        link = payment.confirmation.confirmation_url
        logger.debug("paiment id: %s", payment.id)
        return (link, payment.id)
    except HTTPError as e:
        logger.error("Ошибка при создании платежа: %s", e)
        raise


def generate_qr_code(payment_url, user_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(payment_url)
    qr.make(fit=True)

    # Создаем картинку QR-кода
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"./media/img/{user_id}code.png")
    return f"./media/img/{user_id}code.png"


async def check_payment_status(payment_id):
    try:
        payment = await to_thread(Payment.find_one, payment_id)
        status = payment.status
        if status == 'succeeded':
            return 1, payment
        elif status == 'pending':
            return 2, payment
        elif status == 'canceled':
            return 0, payment
        else:
            return -1, payment
    except Exception as e:
        logger.error("Ошибка при проверке статуса платежа: %s", e)
        raise

@router.callback_query(lambda callback_query: 'check_status' in callback_query.data)
async def check_status_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    id = callback.data.split('_')[-1]
    status = check_payment_status(id)
    print(status)
    if status == 1:
        users = await get_trainer_users(callback.from_user.id)
        for user_id in users:
            await bot.send_message(user_id, BOT_INACTIVE_MESSAGES[0])
        data = await state.get_data()
        await add_subscription(callback.from_user.id, data["sub_days"])
        await callback.message.answer(BOT_ACTIVE_MESSAGE[1], reply_markup=kbi.main())
    elif status == 2:
        await callback.message.answer("Платеж ожидает оплаты")
    elif status == 0:
        await callback.message.answer("Платеж отменен", reply_markup=kbi.main())
    elif status == -1:
        await callback.message.answer("Возникла непредвиденная ошибка", reply_markup=kbi.main())

@router.callback_query(lambda callback_query: 'check_status' in callback_query.data)
async def chec_status_handler(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user
    payment_id = callback.data.split('_')[-1]

    status, payment = await check_payment_status(payment_id)
    payment_method = payment.payment_method

    logger.debug("Status: %s", status)
    logger.debug("Payment method id: %s", payment_method["id"])

    if status == 1:
        logger.debug("payment saved: %s", payment_method["saved"])
        if payment_method["saved"]:
            await save_user_payment(user.id, payment_method["id"])
            await callback.message.answer("Платежные данные сохранены")

        await change_sub_not(user.id, 0)
        data = await state.get_data()
        await add_subscription(user.id, data["sub_days"])

        await callback.message.answer(
            "✅ Подписка успешно оформлена\n"
            "Тебе доступен весь функционал бота. Успешного достижения целей!",
            reply_markup=kbi.main()
        )

    elif status == 2:
        await callback.message.answer("Платеж ожидает оплаты")
    elif status == 0:
        await callback.message.answer("Платеж отменен", reply_markup=kbi.main())
    elif status == -1:
        await callback.message.answer("Возникла непредвиденная ошибка", reply_markup=kbi.main())


@router.message(F.text == "Оплата подписки")
@router.message(F.text == "w")
async def choose_pay_handler(message: Message):
    await message.answer(BOT_INACTIVE_MESSAGES[0], reply_markup=kbr.main())
    await message.answer(BOT_INACTIVE_MESSAGES[1], reply_markup=kbi.choose_pay())

@router.callback_query(F.data == "plus_sub")
async def plus_sub(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(BOT_INACTIVE_MESSAGES[0], reply_markup=kbr.main())
    await callback.message.answer(BOT_INACTIVE_MESSAGES[1], reply_markup=kbi.choose_pay())

async def pay_def(callback: CallbackQuery, state: FSMContext, days=30, price="MONTH_PRICE", is_admin=False):
    await state.update_data(sub_days=days)
    email = await get_user_email(callback.from_user.id)
    if email is None:
        await callback.message.answer("У тебя не установлена почта, напиши её мне, чтобы оплатить")
        await state.set_state(user_data.email)
        return
    payment_data = await create_payment(PRICES[price], email)
    payment_url = payment_data[0]
    
    
    # Генерируем QR-код для платежа
    if is_admin:
        qr_code_path = generate_qr_code(payment_url, callback.from_user.id)
    else:
        qr_code_path = generate_qr_code(payment_url, callback.message.from_user.id)

    # Отправляем QR-код
    if is_admin:
        await callback.answer_photo(
            FSInputFile(path=qr_code_path),
            caption=PAYMENT_MESSAGES[0].format(PRICES[price]["amount"], PRICES[price]["description"], payment_url),
            reply_markup=kbi.pay_status(payment_data[1])
            )
    else:
        await callback.message.answer_photo(
        FSInputFile(path=qr_code_path),
        caption=PAYMENT_MESSAGES[0].format(PRICES[price]["amount"], PRICES[price]["description"], payment_url),
        reply_markup=kbi.pay_status(payment_data[1])
        )

async def start_payment(message: Message):
    text = (
        "Перед оплатой вам нужно принять условия оферты и согласиться на автосписания.\n\n"
        "✅ [Оферта](https://clck.ru/3GYCiN)\n"
       # "✅ [Политика автосписаний](https://your-site.com/autopayments)\n\n"
        "Нажимая кнопку ниже, вы соглашаетесь с условиями."
    )
    buttons = [
        types.InlineKeyboardButton(text="Принимаю условия", callback_data="accept_terms")
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


@router.callback_query(F.data == "accept_terms")
async def on_accept_terms(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await save_user_consent(callback_query.from_user.id, 1)
    # Можно сохранить факт согласия в базу
    # save_user_consent(callback_query.from_user.id)

    await callback_query.message.answer("Спасибо! Теперь переходим к оплате.")
    # Здесь вызываем создание платежа
    if data["sub_days"] == 30:
        await month_pay(callback_query, state)
    elif data["sub_days"] == 90:
        await three_month_pay(callback_query, state)


@router.message(F.text == "admin_pay_def")
async def admin_pay_handler(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await pay_def(message, state, 0, "ADMIN_PRICE", True)


@router.callback_query(F.data == "pay_month")
async def month_pay(callback: CallbackQuery, state: FSMContext):
    auto = await get_user_consent(callback.from_user.id)
    await state.update_data(sub_days=30, auto=auto)
    if auto is None or int(auto[1]) == 0:
        await start_payment(callback.message)
        return
    await pay_def(callback, state, 30, "MONTH_PRICE")


@router.callback_query(F.data == "pay_3_month")
async def three_month_pay(callback: CallbackQuery, state: FSMContext):
    auto = await get_user_consent(callback.from_user.id)
    await state.update_data(sub_days=90, auto=auto)
    if auto is None or int(auto[1]) == 0:
        await start_payment(callback.message)
        return
    await pay_def(callback, state, 90, "THREE_MONTH_PRICE")


@router.callback_query(F.data == "return_to_pay")
async def ret_to_pay(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["sub_days"] == 30:
        await month_pay(callback, state)
    elif data["sub_days"] == 90:
        await three_month_pay(callback, state)


async def sub12hour(user_id):
    user = await get_subscription(user_id)
    if int(user[1]) == 0 and int(user[3]) == 0:
        await bot.send_message(user_id, "Твой тестовый доступ закончился. Чтобы продолжить считать калории и планировать питание, выбери подписку 🎟️", reply_markup=kbi.add_sub_12time())

async def sub72hour(user_id):
    user = await get_subscription(user_id)
    if int(user[1]) == 0 and int(user[3]) == 0:
        await bot.send_message(user_id, "Не хочется считать калории вручную? Но ты все еще хочешь добиться цели? Мы поможем - выбери подписку! 🎯", reply_markup=kbi.add_sub_12time())

async def sub7day(user_id):
    user = await get_subscription(user_id)
    if int(user[1]) == 0 and int(user[3]) == 0:
        await bot.send_message(user_id, "Ты можешь вернуться в любой момент! Мы сохранили твои данные 📊", reply_markup=kbi.add_sub_12time())
        
async def sub21day(user_id):
    user = await get_subscription(user_id)
    if int(user[1]) == 0:
        await add_subscription(user_id, 3)
        await bot.send_message(
            user_id, 
            "Мы дарим тебе еще 3 дня бесплатного использования! Привет, мы знаем, ты сильный и можешь достичь своей цели! Если ты всё еще веришь в себя и готов продолжать, мы готовы помочь тебе на каждом шаге 💪", 
            reply_markup=kbi.back_to_sub())

@router.callback_query(F.data == "no_sub")
async def no_sub(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, мы ждем твоего возвращения, как будешь готов - жми "Продлить доступ"', reply_markup=kbi.add_sub_time_s())


@router.callback_query(F.data == "off_sub")
async def no_sub_s(callback: CallbackQuery, state: FSMContext):
    await change_sub_not(callback.from_user.id, 1)
    await callback.message.answer('Хорошо, мы ждем твоего возвращения, как будешь готов - жми "Продлить доступ"', reply_markup=kbi.add_sub_time_s())
    

async def handle_subscription_end(user_id):
    scheduler.add_job(sub12hour, 'date', run_date=datetime.today() + timedelta(hours=12), args=[user_id])
    scheduler.add_job(sub72hour, 'date', run_date=datetime.today() + timedelta(hours=72), args=[user_id])
    scheduler.add_job(sub7day, 'date', run_date=datetime.today() + timedelta(days=7), args=[user_id])
    scheduler.add_job(sub21day, 'date', run_date=datetime.today() + timedelta(days=21), args=[user_id])

    try:
        scheduler.start()
    except Exception as e:
        logger.warning(e)


async def auto_payment(user_id, amount, desc, days):
    user_payment = await get_user_payment(user_id)
    print(user_payment)
    idempotence_key = str(uuid.uuid4())
    if user_payment is None:
        return False
    email = await get_user_email(user_id)
    
    # Создаем платеж с сохранением метода оплаты
    payment = Payment.create({
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "payment_method_id": user_payment[1],
        "description": f"{desc}, {email}",
        "capture": True,
        "receipt": {
            "customer": {
                "email": email
            },
            "items": [
                {
                    "description": desc,
                    "quantity": "1.00",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "vat_code": 1  # Код НДС (1 означает 20%)
                }
            ]
        },
        "metadata": {
            "cms_name": "yookassa_sdk_python"
        },
        "saved": True  # Сохраняем метод оплаты
    }, idempotence_key)

    # Проверяем статус платежа
    payment = Payment.find_one(payment.id)

    while True:
        if payment.status == "succeeded":
            await change_sub_not(user_id, 0)
            await add_subscription(user_id, days)
            return True
        elif payment.status == "pending":
            await asyncio.sleep(5)
        elif payment.status == "canceled":
            return False


async def task():
    today_utc = datetime.utcnow().date()
    users = await get_all_subscription()
    for user in users:
        if user[1] == "1" and str(today_utc) == user[2]:
            await off_subscription(int(user[0]))
            try:
                print(user[0])
                if int(user[0]) == ADMIN_ID:
                    print("admin")
                    msg = '123'
                    amount = 1
                    desc = 'админская подписка'
                    days = 0
                days = 30
                amount = 1290
                desc = 'Подписка на месяц для тренера'
                msg = BOT_INACTIVE_MESSAGES[1]
                await handle_subscription_end(user[0])
                auto_payment_status = await auto_payment(user[0], amount, desc, days)
                if auto_payment_status:
                    await bot.send_message(int(user[0]), "✅ Автоплатеж прошел успешно")
                    await change_sub_not(int(user[0]), 0)
                    await add_subscription(int(user[0]), days)

                    await bot.send_message(
                        int(user[0]),
                        "✅ Подписка успешно оформлена\n"+
                        "Тебе доступен весь функционал бота. Успешного достижения целей!",
                        reply_markup=kbi.main()
                        )
                else:

                    await bot.send_message(int(user[0]), "Твоя подписка закончилась")
                    await bot.send_message(int(user[0]), BOT_INACTIVE_MESSAGES[0])
                    await bot.send_message(int(user[0]), msg, reply_markup=kbi.choose_pay())
            except:
                logger.warning("Ошибка при отправке сообщения пользователю с id %s", user[0], exc_info=True)
            
        if  user[1] == "1" and str(datetime.today() + timedelta(days=1)) == user[2]:
            await bot.send_message(
                int(user[0]), 
                "Твоя подписка закончится завтра, не забудь пополнить баланс и продлить её, чтобы продолжать пользоваться ботом! 🎟️",
                reply_markup=kbi.main()
            )

@router.message(F.text == "l")
async def l(message: Message):
    await handle_subscription_end(message.from_user.id)


async def my_function(user_id, bot):
    await bot.send_message(user_id, BOT_INACTIVE_MESSAGES[3], reply_markup=kbi.choose_pay())

async def schedule_once_every_7_days(user_id, bot: Bot):
    # Рассчитываем дату следующего запуска через 7 дней
    next_run = datetime.now() + timedelta(days=7)

    # Добавляем задачу в расписание
    scheduler.add_job(my_function(user_id, bot), 'date', run_date=next_run, misfire_grace_time=False)

    # Запускаем расписание
    scheduler.start()

    # Ждем завершения работы
    await scheduler.shutdown()


async def start_scheduler_sub():
    scheduler.add_job(task, 'interval', minutes=1)
    scheduler.start()
