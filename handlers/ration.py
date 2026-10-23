from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import datetime
from middlewares.is_group import PrivateChatMiddleware

from keyboards import reply as kbr
from fsm.states import ration_form, Statistics
from db_methods.progres import update_weight
from db_methods.goals_methods import get_user_goal, add_ration
from db_methods.user_methods import add_age, add_sex, add_height, add_weight
from gpt_models import gen
from text.messages import *


router = Router()
router.message.middleware(PrivateChatMiddleware())

level_or_sport = {
1 : 'Новичок: Я только начал заниматься спортом или физической активностью, у меня нет опыта тренировок в зале.',
2 : 'Умеренный: Я иногда занимаюсь спортом или физической активностью, но без регулярности. Мой опыт тренировок в зале невелик или отсутствует.',
3 : 'Опытный: Я регулярно занимаюсь спортом или физической активностью, включая тренировки в зале. У меня есть опыт выполнения базовых упражнений с гантелями или штангой.',
4 : 'Продвинутый: Я занимаюсь спортом или физической активностью на продвинутом уровне и имею значительный опыт тренировок в зале. Могу выполнять сложные упражнения с большими весами.'
}

@router.message(F.text == 'Изменить рацион')
async def set_ration(message: Message, state: FSMContext) -> None:
    await state.set_state(ration_form.age)
    await message.answer("Для составления рациона питания на неделю, ответь на 9 вопросов, поочерёдно.", reply_markup=kbr.main())
    await message.answer(RATION_FORM_QUESTIONS[0],)


@router.message(F.text == 'Рацион')
async def get_ration(message: Message, state: FSMContext) -> None:
    goals = await get_user_goal(message.from_user.id)
    
    if goals[6]:
        ration = goals[6]
        i = ration.index('\n5.')
        await message.answer('Вот твой текущий рацион питания, хочешь его изменить?')
        await message.answer(text=ration[i:], reply_markup=kbr.ration())
        await message.answer(text=ration[:i])
    else:
        await set_ration(message, state)

@router.callback_query(F.data == 'ration')
async def set_data_ration(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    await set_ration(message, state)


@router.message(ration_form.age, F.text)
async def age_handler(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Пожалуста, корректно введите свой возраст, написав только одно число: колличество полных лет")
    else:
        await state.update_data(k1=message.text)
        await state.update_data(age=message.text)
        await add_age(message.text, message.from_user.id)
        await state.set_state(ration_form.sex)
        await message.answer(RATION_FORM_QUESTIONS[1], reply_markup=kbr.sex())


@router.message(ration_form.sex, F.text)
async def sex_handler(message: Message, state: FSMContext) -> None:
    if message.text not in ["М", "Ж"]:
        await message.answer("Пожалуста, выберите один из предложаных вариантов на кнопках")
    else:
        await state.update_data(k2=message.text)
        await state.update_data(sex=message.text)
        await add_sex(message.text, message.from_user.id)
        await state.set_state(ration_form.height)
        await message.answer(RATION_FORM_QUESTIONS[2], reply_markup=ReplyKeyboardRemove())


@router.message(ration_form.height, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Пожалуста, корректно введите свой рост, написав только одно число: свой рост в см")
    else:
        await state.update_data(k3=message.text)
        await state.update_data(height=message.text)
        await add_height(message.text, message.from_user.id)
        await state.set_state(ration_form.weight)
        await message.answer(RATION_FORM_QUESTIONS[3])


@router.message(ration_form.weight, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Пожалуста, корректно введите свой вес, написав только одно число: полный вес в кг")
    else:
        await state.update_data(k4=message.text)
        await state.update_data(weight=message.text)
        if len(Statistics.data_arr) != 0:
            Statistics.data_arr.append(message.text)
            Statistics.arr.append(str(datetime.date.today()))
        await add_weight(message.text, message.from_user.id)
        await update_weight(message.from_user.id, message.text)
        await state.set_state(ration_form.goal)
        await message.answer(RATION_FORM_QUESTIONS[4])


@router.message(ration_form.goal, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(goal=message.text)
    await state.update_data(k5=message.text)
    await state.set_state(ration_form.food_cancel)
    await message.answer(RATION_FORM_QUESTIONS[5], reply_markup=kbr.no())


@router.message(ration_form.food_cancel, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(cancel=message.text)
    await state.update_data(k6=message.text)
    await state.set_state(ration_form.sport_lvl)
    await message.answer(RATION_FORM_QUESTIONS[6], reply_markup=kbr.sport_lvl())
    await message.answer(
        f'1 - 🟩{level_or_sport[1]}\n\n'+
        f'2 - 🟨{level_or_sport[2]}\n\n'+
        f'3 - 🟧{level_or_sport[3]}\n\n'+
        f'4 - 🟥{level_or_sport[4]}')   


@router.message(ration_form.sport_lvl, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    if message.text in ['1', '2', '3', '4']:
        await state.update_data(sport_lvl=level_or_sport[int(message.text)])
        await state.update_data(k7=level_or_sport[int(message.text)])
    else:
        await state.update_data(sport_lvl=message.text)
        await state.update_data(k7=message.text)
    await state.set_state(ration_form.eat_count)
    await message.answer(RATION_FORM_QUESTIONS[7])


@router.message(ration_form.eat_count, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(eat_count=message.text)
    await state.update_data(k8=message.text)
    await state.set_state(ration_form.comment)
    await message.answer(RATION_FORM_QUESTIONS[8], reply_markup=kbr.no())


@router.message(ration_form.comment, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(comment=message.text)
    await state.update_data(k9=message.text)
    await message.answer(RATION_FORM_QUESTIONS[9])
    data = await state.get_data()
    ans = await gen.generate_ration(data)
    await state.clear()
    answer_ration = ans[0]
    answer_goals = ans[1]
    if len(answer_goals) != 4:
        await message.answer(answer_ration)
    else:
        print('----------------------------------------')
        print(answer_ration)
        await add_ration(answer_ration, message.from_user.id, answer_goals[0], answer_goals[1], answer_goals[2], answer_goals[3] )
        i = answer_ration.index('\n5.')
        
        await message.answer(text=answer_ration[i:], reply_markup=kbr.ration())
        await message.answer(text=answer_ration[:i])
        # kbut2 = InlineKeyboardButton(text="Главная", callback_data="main")
        # kbut1 = InlineKeyboardButton(text="План тренировок", callback_data="tren")
        # keyboard = InlineKeyboardMarkup(inline_keyboard=[[kbut1, kbut2]])
        await message.answer(
            'Для достижения цели эффективно и быстро нужно ещё и тренироваться 💪\n\n'+
            'Составить тебе план тренировок для дома или зала ? - нажми кнопку |План тренировок|\n'+
            'Или пока ограничимся только питанием ?- нажми кнопку |Главная|',
            reply_markup=kbr.gum())
