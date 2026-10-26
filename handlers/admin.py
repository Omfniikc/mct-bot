from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    FSInputFile,
)

from keyboards import inline as kbi
from keyboards import reply as kbr
from middlewares.is_group import PrivateChatMiddleware
from middlewares.is_admin import AdminFilter
from db_methods.user_methods import add_trainer, get_all_user_id, get_referral_statistics, do_sql
from fsm.states import newslater, admin_panel

import os



router = Router()
router.message.middleware(PrivateChatMiddleware())
router.message.middleware(AdminFilter())


@router.message(F.text == "Статистика по рефералам")
async def referral_statistics_handler(message: Message, state: FSMContext):
    await message.answer(
        "Введите User ID пользователя, по которому хотите получить статистику",
        reply_markup=kbi.main() # Функция для получения клавиатуры с пользователями
    )
    await state.set_state(admin_panel.referral_statistics)

@router.message(admin_panel.referral_statistics)
async def get_referral_statistics_handler(message: Message, state: FSMContext):
    user_id = message.text.strip()
    
    if user_id.isdigit():
        user_id = int(user_id)
        referrals = await get_referral_statistics(user_id)

        if referrals:
            referral_count = len(referrals)
            referral_list = "\n".join([f"User ID: {referral[0]}" for referral in referrals])
            await message.answer(
                f"Всего рефералов: {referral_count}\n\nСписок рефералов:\n{referral_list}",
                reply_markup=kbi.main()
            )
        else:
            await message.answer("У данного пользователя нет рефералов.", reply_markup=kbi.main())
    else:
        await message.answer("Пожалуйста, введите корректный User ID.", reply_markup=kbi.main())


@router.message(F.text == "База данных")
async def db_func_handler(message: Message):
    await message.answer("Выбери функцию", reply_markup=kbr.db_admin())


@router.message(F.text == "Получить базу данных")
@router.message(F.text == "get db")
async def get_db_handler(message: Message, state: FSMContext):
    await message.answer_document(types.FSInputFile(path='./main.db'),
                                  caption="Актульная база данных", reply_markup=kbi.main())
    
@router.message(F.text == "Загрузить базу данных")
async def put_db_handler(message: Message, state: FSMContext):
    await message.answer("Отправьте файл базы данных", reply_markup=kbi.main())
    await state.set_state(admin_panel.upload_db)

@router.message(admin_panel.upload_db, F.document)
async def handle_upload_db(message: Message, state: FSMContext, bot: Bot):
    document = message.document
    if document.file_name.endswith('.db'):
        file = await bot.get_file(document.file_id)
        file_path = './main.db'
        os.remove(file_path)
        await bot.download_file(file.file_path, destination=file_path)
        await message.answer("База данных успешно загружена", reply_markup=kbi.main())
    else:
        await message.answer("Неверный формат файла. Пожалуйста, загрузите файл базы данных в формате .db", reply_markup=kbi.main())
    await state.clear()


@router.message(F.text == "Сделать sql запрос")
async def sql_query_handler(message: Message, state: FSMContext):
    await message.answer("Напиши sql запрос", reply_markup=kbi.main())
    await state.set_state(admin_panel.sql_query)

@router.message(admin_panel.sql_query, F.text)
async def handle_sql_query(message: Message, state: FSMContext):
    sql_query = message.text
    try:
        await do_sql(sql_query)
        await message.answer("SQL запрос выполнен", reply_markup=kbi.main())
    except Exception as e:
        await message.answer(f"Ошибка при выполнении SQL запроса: {e}", reply_markup=kbi.main())
    await state.clear()


@router.message(F.text == "Добавить тренера")
@router.message(F.text == "add admin")
async def get_trainer_id_handler(message: Message, state: FSMContext):
    await message.answer(
        "Введиет айди пользователя, которого сделать тренером и через пробел количество дней, добавляемых к подписке",
        reply_markup=kbi.main())
    await state.set_state(admin_panel.add_trainer)

@router.message(admin_panel.add_trainer)
async def add_trainer_handler(message: Message, state: FSMContext):
    user_id = message.text.split()[0]
    days = message.text.split()[1]
    await add_trainer(user_id, days)
    await message.answer("Тренер добавлен", reply_markup=kbi.main())


@router.message(F.text == "Запустить массовую рассылку")
@router.message(F.text == "asd")
async def get_message_news(message: Message , state: FSMContext):
    await message.answer(
        "Введите сообщение которое необходимо отправить пользователям",
        relpy_markup=kbi.main())
    await state.set_state(newslater.message)


@router.message(newslater.message)
async def send_all_messages(message: Message, state: FSMContext):
    await state.set_state(newslater.ready)
    await state.update_data(mess = message.text)
    await message.answer(
        f"Отправить такое сообщение всем пользователям?\n\n\n{message.text}",
        reply_markup=kbr.yes_no())

@router.message(newslater.ready)
async def done_send(message: Message, state: FSMContext, bot: Bot):
    text = message.text.lower()
    data = await state.get_data()
    if text == 'да':
        await message.answer("Сообщения отправляются")
        users = await get_all_user_id()
        for user in users:
            try:
                await bot.send_message(user, data["mess"])
            except:
                print(f"сообщение не отправлено пользователю {user}")
        await message.answer("Сообщение было отправлено всем пользователям", reply_markup=kbi.main())
    if text == 'нет':
        await message.answer("Введите измененное сообщение", reply_markup=kbi.main())
        await state.set_state(newslater.message)

@router.message(F.text == "Админпанель")
async def admin_panel_handler(message: Message, state: FSMContext):
    await message.answer("Выберите действие", reply_markup=kbr.admin_panel())

@router.message(F.text == "Запустить рассылку")
async def point_newslater(message: Message, state: FSMContext):
    await message.answer("Напиши все айди через пробел, кому отправить сообщение")
    await state.set_state(newslater.point_users)

@router.message(newslater.point_users, F.text)
async def point_get_users(message: Message, state: FSMContext):
    users = message.text.split()
    await state.update_data(users=users)
    await message.answer("Теперь Введите сообщение, которое хотите отправить")
    await state.set_state(newslater.point_message)

@router.message(newslater.point_message)
async def send_point_messages(message: Message, state: FSMContext):
    await state.set_state(newslater.point_ready)
    data = await state.get_data()
    await state.update_data(mess=message.text)
    await message.answer(
        f"Отправить такое сообщение  пользователям\n{'\n'.join(data["users"])}\n?\n\n\n{message.text}",
        reply_markup=kbr.yes_no())

@router.message(newslater.point_ready)
async def done_send(message: Message, state: FSMContext, bot: Bot):
    text = message.text.lower()
    data = await state.get_data()
    if text == 'да':
        await message.answer("Сообщения отправляются")
        users = data["users"]
        for user in users:
            try:
                await bot.send_message(user, data["mess"])
            except:
                print(f"сообщение не отправлено пользователю {user}")
        await message.answer("Сообщение было отправлено всем пользователям", reply_markup=kbi.main())
    if text == 'нет':
        await message.answer("Введите измененное сообщение", reply_markup=kbi.main())
        await state.set_state(newslater.point_message)


@router.message(F.text == "Получить фото")
async def get_photo_path(message: Message, state: FSMContext):
    await message.answer("Отправь полный путь до фото", reply_markup=kbi.main())
    await state.set_state(admin_panel.get_photo)

@router.message(admin_panel.get_photo)
async def send_photo(message: Message, state: FSMContext):
    try:
        await message.answer_photo(FSInputFile(path=message.text), reply_markup=kbi.main())
    except:
        await message.answer("Не удалосьс отправить фото по этому пути", reply_markup=kbi.main())

