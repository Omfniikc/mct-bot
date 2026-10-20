from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import reply as kbr
from fsm.states import goals, main_menu
from middlewares.is_group import PrivateChatMiddleware
from db_methods import goals_methods as bd


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text == "Изменить цели")
async def set_goals(message: Message, state: FSMContext):
    await state.set_state(goals.set_menu)
    await message.answer(
        "Какую цель хочешь отредактировать:",
        reply_markup=kbr.set_goals()
    )

@router.message(lambda message: message.text and 'Мои планы' in message.text)
async def plans(message: Message, state: FSMContext) -> None:
    await state.set_state(main_menu.plans)
    await message.answer(
        'Здесь можно составить или посмотреть твои индивидуальные рацион питания и план тренировок.\n'+
        'Выбери что нужно:',
        reply_markup=kbr.plans()
    )

@router.message(goals.set_menu, F.text == "Цель по калориям")
async def set_kcal(message: Message, state: FSMContext):
    await state.set_state(goals.kcal)
    await message.answer("Введите желаемое количество калорий на день", reply_markup=kbr.main())

@router.message(goals.set_menu, F.text == "Цель по белкам")
async def set_protein(message: Message, state: FSMContext):
    await state.set_state(goals.protein)
    await message.answer("Введите желаемое количество белков на день", reply_markup=kbr.main())

@router.message(goals.set_menu, F.text == "Цель по весу")
async def set_weight(message: Message, state: FSMContext):
    await state.set_state(goals.weight)
    await message.answer("Введите желаемый вес", reply_markup=kbr.main())

@router.message(goals.set_menu, F.text == "Цель по жирам")
async def set_weight(message: Message, state: FSMContext):
    await state.set_state(goals.fat)
    await message.answer("Введите желаемое количество жиров на день", reply_markup=kbr.main())

@router.message(goals.set_menu, F.text == "Цель по углеводам")
async def set_weight(message: Message, state: FSMContext):
    await state.set_state(goals.carbohydrate)
    await message.answer("Введите желаемое количество углеводов на день", reply_markup=kbr.main())

@router.message(lambda message: message.text and ('Цель' in message.text or 'Изменить цель по калориям' in message.text))
async def process_name(message: Message, state: FSMContext) -> None:
    await set_kcal(message, state)

@router.message(lambda message: message.text and 'Изменить цель по весу' in message.text)
async def process_weight(message: Message, state: FSMContext) -> None:
    weight = await bd.get_user_goal(message.from_user.id)[5]

    if weight == "0":
        await message.answer('Введите новую цель по весу в кг')
        await state.set_state(goals.weight)
    else:
        await message.answer(
            f"Текущая цель по весу: {weight} кг\nХотите её изменить?",
            reply_markup=kbr.weight_goal())

@router.message(lambda message: message.text and 'Да, изменить' in message.text)
async def process_weight(message: Message, state: FSMContext) -> None:
    await state.set_state(goals.weight)
    await message.answer('Введи новую цель по весу в кг')
        
@router.message(goals.kcal, F.text)
async def process_goal(message: Message, state: FSMContext) -> None:
    goal = message.text
    await bd.add_goal_kcal(goal, message.from_user.id)
    await state.clear()
    await message.answer(
        'Ваша цель по количеству калорий успешно установлена!',
        reply_markup=kbr.main())
    

@router.message(goals.carbohydrate, F.text)
async def get_carbohydrate(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await bd.update_carbohydrate(message.from_user.id, message.text)
        await message.answer("✅Данные заданы", reply_markup=kbr.main())

@router.message(goals.weight, F.text)
async def get_weight(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await bd.update_weight(message.from_user.id, message.text)
        await message.answer("✅Данные заданы", reply_markup=kbr.main())

@router.message(goals.fat, F.text)
async def get_fat(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await bd.update_fat(message.from_user.id, message.text)
        await message.answer("✅Данные заданы", reply_markup=kbr.main())

@router.message(goals.kcal, F.text)
async def get_kcal(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await bd.update_kcal(message.from_user.id, message.text)
        await message.answer("✅Данные заданы", reply_markup=kbr.main())

@router.message(goals.protein, F.text)
async def get_protein(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напишите только число, ничего больше")
    else:
        await bd.update_protein(message.from_user.id, message.text)
        await message.answer("✅Данные заданы", reply_markup=kbr.main())
