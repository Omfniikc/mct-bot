from aiogram import Router, F
from aiogram.types import Message
from keyboards import inline as kbi
from keyboards import reply as kbr
from fsm.states import main_menu, measurements
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from db_methods.user_methods import add_measurements_figure, add_measurements_power, get_measurements_power, get_measurements_figure
from db_methods.progres import update_weight, get_all_weight
from text.lists import MEASUREMENTS
router = Router()



@router.message(F.text == "Замеры", main_menu.add_food)
async def measurements_menu(message: Message, state: FSMContext):
    await message.answer("Какие данные хотите добавить", reply_markup=kbr.measurements())
    await state.set_state(measurements.menu)

@router.message(measurements.menu)
async def measurements_menu(message: Message, state: FSMContext):
    if message.text == "Вес":
        await view_weight_statistics_handler(message, state)
        await state.set_state(measurements.weight)
    elif message.text == "Фигура":
        await message.answer("Выбери что замеряем", reply_markup=kbi.figure())
        await state.set_state(measurements.figure)
    elif message.text == "Силовые":
        await message.answer("Выбери что замеряем", reply_markup=kbi.power())
        await state.set_state(measurements.power)
        

@router.callback_query(measurements.figure)
async def figure(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
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
        
        

@router.callback_query(measurements.power)
async def power(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
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

    await callback.message.answer(text, reply_markup=kbi.add_measurements())
    await state.set_state(measurements.power_stat)


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

    await callback.message.answer(text, reply_markup=kbi.add_measurements())
    await state.set_state(measurements.figure_stat)

async def view_weight_statistics_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await get_all_weight(user_id)
    await message.answer("Статистика по весу:")
    if not data:
        text = "У вас пока нет замеров"
    else:
        text = ""
        for i in data:
            s = f"{i[2]} - {i[3]}\n\n"
            text += s

    await message.answer(text, reply_markup=kbi.add_measurements())

@router.callback_query(measurements.weight, F.data == "add_measurements")
async def add_measurements_weight_handler(callback: CallbackQuery, state: FSMContext):
    data_s = await state.get_data()
    await callback.message.answer(f"Введи вес в формате вес в кг, можно с точность до десятых, например: 65,7", reply_markup=kbi.main())
    await state.set_state(measurements.add_weight)


@router.callback_query(measurements.power_stat, F.data == "add_measurements")
async def add_measurements_power_handler(callback: CallbackQuery, state: FSMContext):
    data_s = await state.get_data()
    await callback.message.answer(f"Введи {MEASUREMENTS[data_s['power']]} в формате вес (в кг)/кол-во повторов, например: 12/20", reply_markup=kbi.main())
    await state.set_state(measurements.add_power)


@router.message(measurements.add_power)
async def add_measurements_power_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data_s = await state.get_data()
    try:
        weight, count = message.text.split('/')
    except:
        await message.answer("Вводите коректное значения, попробуйете снова")
        return
    if weight.isdigit() and count.isdigit():
        await add_measurements_power(user_id, data_s["power"], weight, count)
        await message.answer("Замер задан\n\nВот твоя статистика:")
        data = await get_measurements_power(user_id, data_s["power"])
        text = ""
        for i in data:
            s = f"{i[2]} - {i[3]}/{i[4]}\n\n"
            text += s

        await message.answer(text, reply_markup=kbi.add_measurements())
    else:
        await message.answer("Вводите коректное значения, попробуйете снова")


@router.callback_query(measurements.figure_stat, F.data == "add_measurements")
async def add_measurements_figure_handler(callback: CallbackQuery, state: FSMContext):
    data_s = await state.get_data()
    await callback.message.answer(f"Введи {MEASUREMENTS[data_s['figure']]} в см, можно с точность до десятых, например: 67,5", reply_markup=kbi.main())
    await state.set_state(measurements.add_figure)


@router.message(measurements.add_figure)
async def add_measurements_figure_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data_s = await state.get_data()
    value = message.text.replace(",", ".")

    try:
        float(value)
        await add_measurements_figure(user_id, data_s["figure"], value)
        await message.answer("Замер задан\n\nВот твоя статистика:")
        data = await get_measurements_figure(user_id, data_s["figure"])
        text = ""
        for i in data:
            s = f"{i[2]} - {i[3]}\n\n"
            text += s
    
        await message.answer(text, reply_markup=kbi.add_measurements())
    except ValueError:
        await message.answer("Вводите корректное значение, попробуйте снова")
        return
    

@router.message(measurements.add_weight)
async def add_measurements_weight_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    weight = message.text.replace(",", ".")
    
    try:
        float(weight)
        await update_weight(user_id, weight)
        await message.answer("Замер веса задан\n\nВот твоя статистика:")
        data = await get_all_weight(user_id)
        text = ""
        for i in data:
            s = f"Дата: {i[2]}, Вес: {i[4]} кг\n\n"
            text += s

        await message.answer(text, reply_markup=kbi.add_measurements())
    except ValueError:
        await message.answer("Вводите корректное значение, попробуйте снова")
        return





