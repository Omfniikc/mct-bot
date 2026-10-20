from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import reply as kbr
from keyboards import inline as kbi
from fsm.states import main_menu, user_data, SubscriptionStates
from db_methods.user_methods import (
    set_notification,
    user_is_notify,
    get_user_info, 
    add_age,
    add_sex,
    add_height,
    add_weight,
    get_subscription,
    is_admin,
    set_email,
    save_user_consent
    )
from middlewares.is_group import PrivateChatMiddleware
from generate.check_time import get_current_time
from db_methods.goals_methods import get_user_goal
from .progres import is_float
from text.messages import *

import re
from datetime import datetime


router = Router()
router.message.middleware(PrivateChatMiddleware())

@router.message(F.text == 'Профиль')
async def profile(message: Message, state: FSMContext) -> None:
    is_trainer = await get_subscription(message.from_user.id)
    is_trainer = True if is_trainer else False
    user_data = await get_user_info(message.from_user.id)
    user_goals = await get_user_goal(message.from_user.id)
    is_notify = await user_is_notify(message.from_user.id)
    is_adm = await is_admin(message.from_user.id)

    notify_text = "Включены" if is_notify else "Отключены"
    notify_text_menu = "Включить уведомления" if not is_notify else "Выключить уведомления"
    sex = user_data[3]
    time = user_data[6]
    age = user_data[4]
    weight = user_data[2]
    height = user_data[5]
    g_k = user_goals[1]
    g_b = user_goals[2]
    g_z = user_goals[3]
    g_y = user_goals[4]
    time_text = f"(GMT +{time})" if int(time) >= 0 else f"(GMT {time})"

    await state.update_data(user_time=time)
    await state.update_data(user_age=age)
    await state.update_data(user_sex=sex)
    await state.update_data(user_height=height)
    await state.update_data(user_weight=weight)

    await message.answer(
        f'👤ПРОФИЛЬ:\n\n'+
        f'<b>Возраст:</b> {age}\n'+
        f'<b>Пол:</b> {sex}\n'+
        f'<b>Рост:</b> {height}\n'+
        f'<b>Вес:</b> {weight}\n\n'+
        '💥Цели:\n'+
        f'<b>По kcal:</b> {g_k} в день\n'+
        f'<b>По белкам:</b> {g_b} г. в день\n'+
        f'<b>По жирам:</b> {g_z} г. в день\n'+
        f'<b>По углеводам:</b> {g_y} г. в день\n\n'+
        '🔘 Другие:\n'+
        f'<b>Часовой пояс:</b> {time_text}\n'+
        f'<b>Уведомления:</b> {notify_text}\n'+
        'Любую обратную связь пишите сюда - @kimonez (баги, неудобства, вопросы и пожелания)',
        parse_mode=ParseMode.HTML,
        reply_markup=kbr.profile(notify_text_menu, is_adm, is_trainer))
    await state.set_state(main_menu.profile)
    print(message.from_user)

@router.message(main_menu.profile, F.text == "Включить уведомления")
async def on_notification(message: Message):
    await set_notification(message.from_user.id, 1)
    await message.answer("Уведомления включены", reply_markup=kbr.main())

@router.message(main_menu.profile, F.text == "Выключить уведомления")
async def on_notification(message: Message):
    await set_notification(message.from_user.id, 0)
    await message.answer("Уведомления выключены", reply_markup=kbr.main())

@router.message(main_menu.profile, F.text == "Изменить данные")
async def set_user_data_menu(message: Message, state: FSMContext) -> None:
    await message.answer("Выбери данные для изменения", reply_markup=kbr.user_data())
    await state.set_state(user_data.menu)


@router.message(user_data.menu, F.text == "Изменить возраст")
async def set_age(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(user_data.set_age)
    await message.answer(
        f"Сейчас у тебя установлен возраст {data['user_age']} лет, если хочешь изменить его, просто напиши мне новый",
        reply_markup=kbr.main()
    )

@router.message(user_data.set_age, F.text)
async def get_new_age(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await add_age(message.text, message.from_user.id)
        await message.answer("Новый возраст установлен", reply_markup=kbr.main())
    else:
        await message.answer("Вводи только свой возраст, например 18", reply_markup=kbr.main())


@router.message(user_data.menu, F.text == "Изменить пол")
async def set_sex(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(user_data.set_sex)
    await message.answer(
        f"Сейчас у теябя установлен {data['user_sex']} пол, если хочешь поменять его, то выбери на клавиатуре",
        reply_markup=kbr.sex()
    )

@router.message(user_data.set_sex, F.text)
async def get_new_sex(message: Message, state: FSMContext) -> None:
    if message.text  in ["М", "Ж"]:
        await add_sex(message.text, message.from_user.id)
        await message.answer("Твой пол задан", reply_markup=kbr.main())
    else:
        await message.answer("Выбири вариант на клавиатуре")


@router.message(user_data.menu, F.text == "Изменить рост")
async def set_height(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(user_data.set_height)
    await message.answer(
        f"Сейчас твой рост задан на {data['user_height']}см, если хочешь указать другой, то просто напиши его мне",
        reply_markup=kbr.main()
    )

@router.message(user_data.set_height, F.text)
async def get_new_height(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await add_height(message.text, message.from_user.id)
        await message.answer("Новый рост установлен", reply_markup=kbr.main())
    else:
        await message.answer("Вводи только свой рост, например 170", reply_markup=kbr.main())


@router.message(user_data.menu, F.text == "Изменить вес")
async def set_weight(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(user_data.set_weight)
    await message.answer(
        f"Сейас твой вес установлен на {data['user_weight']}кг, если хочешь его изменить, то просто напиши его мне",
        reply_markup=kbr.main()
    )

@router.message(user_data.set_weight, F.text)
async def get_new_weight(message: Message, state: FSMContext) -> None:
    if is_float(message.text):
        await add_weight(message.text, message.from_user.id)
        await message.answer("Новый вес установлен", reply_markup=kbr.main())
    else:
        await message.answer("Вводи свой вес с точночностью до десятых, например 60.54", reply_markup=kbr.main())

 
@router.message(user_data.menu, F.text == "Изменить часовой пояс")
async def set_time(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    time = get_current_time(int(data["user_time"]))
    await state.set_state(user_data.set_time)
    await message.answer(
        START_MESSAGES[5].format(time, data['user_time']),
        reply_markup=kbi.user_gmt()
    )

@router.message(user_data.email, F.text)
async def set_email_handler(message: Message, state: FSMContext):
    email = message.text
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if bool(re.match(email_pattern, email)):
        await message.answer(f"Твоя почта: {email}?", reply_markup=kbi.yes_no())
        await state.update_data(email=email)
    else:
        await message.answer("Вводи корректный адрес почты")

@router.callback_query(user_data.email, F.data)
async def upd_email_handler(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    if callback.data == "yes":
        data = await state.get_data()
        email = data["email"]
        await set_email(email, callback.from_user.id)
        await message.answer("Почта сохранена", reply_markup=kbi.return_to_pay())
    elif callback.data == "no":
        await message.answer("Введи почту заново", reply_markup=kbr.main())

@router.message(F.text == "Моя подписка")
async def my_sub_handler(message: Message, state: FSMContext):
    sub_data = await get_subscription(message.from_user.id)
    if not sub_data:
        await message.answer('Вы должны быть подключены к тренеру', reply_markup=kbi.main())
        return
    if int(sub_data[1]) == 0:
        await message.answer('''
Подписка не активна ❌
                            
Ты можешь оформить ее прямо здесь, и получишь неограниченное число распознаваний по фото, голосу и тексту, доступ к статистике за день и главное - приблизишься к цели ⚡️
                             ''', reply_markup=kbr.main())
        await message.answer(BOT_INACTIVE_MESSAGES[1], reply_markup=kbi.choose_pay())
    else:
        sub_date = datetime.strftime(datetime.strptime(sub_data[2], "%Y-%m-%d"), "%d.%m.%y")
        await message.answer(f'''
Подписка активна до {sub_date} ✅

У тебя хорошо получается следить за питанием!

Ты можешь отказаться от подписки на следующий период, нажав кнопку "Отменить подписку"
                             ''', reply_markup=kbi.subscription())
        await state.set_state(SubscriptionStates.sub)
        await state.update_data(sub_date=sub_date)


@router.callback_query(SubscriptionStates.sub, F.data == "cancel")
async def cancel_subscription_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        "Ты точно хочешь отменить подписку?\n\n"
        f"Ты сможешь пользоваться ботом до {data["sub_date"]}, но потом мы не сможем помогать тебе с питанием 😢",
        reply_markup=kbi.cancel_subscription()
    )
    await state.set_state(SubscriptionStates.confirm_cancel)

@router.callback_query(SubscriptionStates.confirm_cancel, F.data == "confirm_cancel")
async def confirm_cancel_subscription(callback: CallbackQuery, state: FSMContext):
    await save_user_consent(callback.from_user.id, 0)
    await callback.message.answer(
        "Твоя подписка отменена.\n\n"
        "Пожалуйста, напиши почему ты решил(а) отменить подписку @kimonez, мы пытаемся сделать сервис лучше и будем очень благодарны",
        reply_markup=kbi.main()
    )
