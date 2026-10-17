from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def back_main():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Назад", callback_data="back")],
            [InlineKeyboardButton(text="Главная", callback_data="main")]
        ])
    return menu



def power():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Подтягивания", callback_data="push_ups")],
            [InlineKeyboardButton(text="Брусья", callback_data="dips")],
            [InlineKeyboardButton(text="Жим лёжа", callback_data="bench_press")],
            [InlineKeyboardButton(text="Махи с гантелями", callback_data="dumbbell_flyes")],
            [InlineKeyboardButton(text="Протяжка на дельты", callback_data="delta_pull")],
            [InlineKeyboardButton(text="Штанга на бицепс", callback_data="barbell_curl")],
            [InlineKeyboardButton(text="Присед со штангой", callback_data="barbell_squat")],
            [InlineKeyboardButton(text="Становая тяга", callback_data="deadlift")],
            [InlineKeyboardButton(text="Жим гантелей на вертикальной скамье", callback_data="dumbbell_overhead_press")],
            [InlineKeyboardButton(text="Жим штанги на вертикальной скамье", callback_data="barbell_overhead_press")]
        ])
    return menu

def add_measurements():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Добавить замер", callback_data="add_measurements")],
            [InlineKeyboardButton(text="Главная", callback_data="main")]
        ])
    return menu


def figure():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Бицепс", callback_data="biceps")],
            [InlineKeyboardButton(text="Талия", callback_data="waist")],
            [InlineKeyboardButton(text="Обхват плеч", callback_data="shoulder")],
            [InlineKeyboardButton(text="Обхват бёдер", callback_data="hips")],
            [InlineKeyboardButton(text="Предплечье", callback_data="forearm")],
            [InlineKeyboardButton(text="Икры", callback_data="back")],
            [InlineKeyboardButton(text="Обхват грудных", callback_data="chest")]
        ])
    return menu


def choose_users_statistic():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Питание", callback_data="choose_user_food")],
            [InlineKeyboardButton(text="Замеры", callback_data="choose_user_measurements")]
        ])
    return menu


def back():
    menu = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return menu

def save_cal():
    menu = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Сохранить", callback_data="save")],
        [InlineKeyboardButton(text="Ввести вручную", callback_data="set")]
    ])
    return menu

def add_client():
    menu = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Добавить Клиента", callback_data="add_client")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return menu

def choose_users(users: dict):
    menu_lst = []
    for user in users:
        menu_lst.append([InlineKeyboardButton(text=user, callback_data=f"user_{users[user]}")])
    menu_lst.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    menu = InlineKeyboardMarkup(inline_keyboard=menu_lst)
    return menu

def measurements_users():
    menu = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Да", callback_data=f"yes"),
            InlineKeyboardButton(text="Назад", callback_data=f"back")
        ],
        [
            InlineKeyboardButton(text="Главная", callback_data=f"main")
        ]
    ])
    return menu

def choose_day():
    menu = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Вчера", callback_data=f"yesterday"),
            InlineKeyboardButton(text="Сегодня", callback_data=f"today")
        ],
        [
            InlineKeyboardButton(text="Выбрать свою дату", callback_data=f"choose_my_date")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ])
    return menu

def user_or_trainer():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Пользователь", callback_data=f"user"),
                InlineKeyboardButton(text="Тренер", callback_data=f"trainer")
            ]
        ])
    return menu

def cancel_redact_food():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
        ])
    return menu

def yes_no():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Да", callback_data=f"yes"),
                InlineKeyboardButton(text="Нет", callback_data=f"no")
            ]
        ])
    return menu

def return_to_pay():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Вернуться к оплате", callback_data=f"return_to_pay")]
        ])
    return menu

def pay_status(id):
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Проверить статус платежа", callback_data=f"check_status_{id}")]
        ])
    return menu 

def admin_add_tren():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Закончить добавление тренировки", callback_data="add_tren")]
        ])
    return menu 

def admin_add_exer():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Посмотреть видео", callback_data="upd_media"),
            InlineKeyboardButton(text="Посмотреть полное описание", callback_data="upd_desc")],
            [InlineKeyboardButton(text="Готово", callback_data="add_exer")]
        ])
    return menu 

def start_exer():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Начать", callback_data="start_exer")]
        ])
    return menu

def wait_tren():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_wait")],
            [InlineKeyboardButton(text="В главное меню", callback_data="main")]
        ])
    return menu

def strikethrough(text):
    return ''.join([char + '\u0336' for char in text])

def choose_pay():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Месяц — {strikethrough('1890')} 1290₽", callback_data="pay_month")],
        [InlineKeyboardButton(text=f"3 месяца — {strikethrough('5670')} 2690₽", callback_data="pay_3_month")]
    ])
    return menu



def notification():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Добавить", callback_data="main")],
            [InlineKeyboardButton(text="Отменить напоминания", callback_data="notify_cancel")]
        ])
    return menu

def true_notify():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Точно отменить", callback_data="notify_true_cancel")],
            [InlineKeyboardButton(text="Не отменять🚀", callback_data="not_cancel_notify")]
        ])
    return menu

def user_gmt(is_start=0):
    if is_start:
        menu = InlineKeyboardMarkup(inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="0", callback_data=f"time_0_start"),
                    InlineKeyboardButton(text="1", callback_data=f"time_1_start"),
                    InlineKeyboardButton(text="2", callback_data=f"time_2_start"),
                    InlineKeyboardButton(text="3", callback_data=f"time_3_start"),
                    InlineKeyboardButton(text="4", callback_data=f"time_4_start"),
                    InlineKeyboardButton(text="5", callback_data=f"time_5_start"),
                    InlineKeyboardButton(text="6", callback_data=f"time_6_start"),
                    InlineKeyboardButton(text="7", callback_data=f"time_7_start")
                ],
                [
                    InlineKeyboardButton(text="8", callback_data=f"time_8_start"),
                    InlineKeyboardButton(text="9", callback_data=f"time_9_start"),
                    InlineKeyboardButton(text="10", callback_data=f"time_10_start"),
                    InlineKeyboardButton(text="11", callback_data=f"time_11_start"),
                    InlineKeyboardButton(text="12", callback_data=f"time_12_start"),
                    InlineKeyboardButton(text="13", callback_data=f"time_13_start"),
                    InlineKeyboardButton(text="14", callback_data=f"time_14_start"),
                    InlineKeyboardButton(text="15", callback_data=f"time_15_start")
                ],
                [
                    InlineKeyboardButton(text="16", callback_data=f"time_16_start"),
                    InlineKeyboardButton(text="17", callback_data=f"time_17_start"),
                    InlineKeyboardButton(text="18", callback_data=f"time_18_start"),
                    InlineKeyboardButton(text="19", callback_data=f"time_19_start"),
                    InlineKeyboardButton(text="20", callback_data=f"time_20_start"),
                    InlineKeyboardButton(text="21", callback_data=f"time_21_start"),
                    InlineKeyboardButton(text="22", callback_data=f"time_22_start"),
                    InlineKeyboardButton(text="23", callback_data=f"time_23_start")
                ],
                [InlineKeyboardButton(text="Пропустить", callback_data=f"main_start")]
            ])
    else:
        menu = InlineKeyboardMarkup(inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="0", callback_data=f"time_0"),
                    InlineKeyboardButton(text="1", callback_data=f"time_1"),
                    InlineKeyboardButton(text="2", callback_data=f"time_2"),
                    InlineKeyboardButton(text="3", callback_data=f"time_3"),
                    InlineKeyboardButton(text="4", callback_data=f"time_4"),
                    InlineKeyboardButton(text="5", callback_data=f"time_5"),
                    InlineKeyboardButton(text="6", callback_data=f"time_6"),
                    InlineKeyboardButton(text="7", callback_data=f"time_7")
                ],
                [
                    InlineKeyboardButton(text="8", callback_data=f"time_8"),
                    InlineKeyboardButton(text="9", callback_data=f"time_9"),
                    InlineKeyboardButton(text="10", callback_data=f"time_10"),
                    InlineKeyboardButton(text="11", callback_data=f"time_11"),
                    InlineKeyboardButton(text="12", callback_data=f"time_12"),
                    InlineKeyboardButton(text="13", callback_data=f"time_13"),
                    InlineKeyboardButton(text="14", callback_data=f"time_14"),
                    InlineKeyboardButton(text="15", callback_data=f"time_15")
                ],
                [
                    InlineKeyboardButton(text="16", callback_data=f"time_16"),
                    InlineKeyboardButton(text="17", callback_data=f"time_17"),
                    InlineKeyboardButton(text="18", callback_data=f"time_18"),
                    InlineKeyboardButton(text="19", callback_data=f"time_19"),
                    InlineKeyboardButton(text="20", callback_data=f"time_20"),
                    InlineKeyboardButton(text="21", callback_data=f"time_21"),
                    InlineKeyboardButton(text="22", callback_data=f"time_22"),
                    InlineKeyboardButton(text="23", callback_data=f"time_23")
                ],
                [InlineKeyboardButton(text="Пропустить", callback_data=f"main")]
            ])
    return menu

def no_del(data):
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Удалить", callback_data=f"deletetrue_{data}")],
            [InlineKeyboardButton(text="Оставить", callback_data=f"deleteno_{data}")]
        ])
    return menu

def ration():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Рацион", callback_data="ration")]
        ])
    return menu


def add_food(data): # Клавиатура, которая высылается с таблицей КБЖУ приёмами пищи
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="💬 Исправить", callback_data=f"correct_{data}"), InlineKeyboardButton(text="❌ Отменить", callback_data=f"delete_{data}")],
            [InlineKeyboardButton(text="Главная", callback_data="main")]
        ])
    return menu


def correct_food(data):
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="💬 Исправить", callback_data=f"correct_{data}"), InlineKeyboardButton(text="❌ Отменить", callback_data=f"delete_{data}")],
        ])
    return menu


def main():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Главная", callback_data="main")]
        ])
    return menu

def back_to_sub():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Возвращаюсь к подписке", callback_data="main")]
        ])
    return menu

def add_food_main():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Посчитать прием пищи", callback_data="main")]
        ])
    return menu

def subscription():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отменить подписку", callback_data="cancel")],
        [InlineKeyboardButton(text="Главная", callback_data="main")]
    ])
    return menu

def cancel_subscription():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Точно отменить", callback_data="confirm_cancel")],
        [InlineKeyboardButton(text="Главная", callback_data="main")]
    ])
    return menu

def add_sub_12time():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Продлить доступ", callback_data=f"plus_sub"),
                InlineKeyboardButton(text="Пока без подписки", callback_data=f"no_sub")
            ]
        ])
    return menu

def add_sub_time():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Продлить доступ", callback_data=f"plus_sub"),
                InlineKeyboardButton(text="Скрыть напоминания", callback_data=f"off_sub")
            ]
        ])
    return menu

def add_sub_time_s():
    menu = InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Продлить доступ", callback_data=f"plus_sub")
            ]
        ])
    return menu