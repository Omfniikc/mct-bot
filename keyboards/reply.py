from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_panel():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="База данных"), KeyboardButton(text="Статистика по рефералам")],
            [KeyboardButton(text="Запустить массовую рассылку"), KeyboardButton(text="Запустить рассылку")],
            [KeyboardButton(text="Получить фото"), KeyboardButton(text="Управление пользователями")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def measurements():
    menu = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Вес")],
            [KeyboardButton(text="Фигура"), KeyboardButton(text="Силовые")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return menu

def trainer_menu():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Статистика по всем клиентам"), KeyboardButton(text="Статистика по клиенту")],
            [KeyboardButton(text="Задать цели для клиента"), KeyboardButton(text="Добавить клиента")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def db_admin():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Получить базу данных"), KeyboardButton(text="Загрузить базу данных")],
            [KeyboardButton(text="Сделать sql запрос")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def admin_users():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Добавить подписку"), KeyboardButton(text="Удалить пользователя")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def start_tren():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Начать")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def exercises():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Готово")],
            [KeyboardButton(text="Пропустить")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def choise_tren():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Тренировка для похудения")],
            [KeyboardButton(text="Тренировка для набора массы")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def progres():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Неделя"), KeyboardButton(text="Месяц"), KeyboardButton(text="Квартал")],
            [KeyboardButton(text="Добавить вес")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def set_goals():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Цель по калориям"), KeyboardButton(text="Цель по белкам")],
            [KeyboardButton(text="Цель по жирам"), KeyboardButton(text="Цель по углеводам")],
            [KeyboardButton(text="Главная")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def profile(notify_text, is_admin, is_sub = False):
    if not is_sub:
        kbr = [
                [
                    KeyboardButton(text="Изменить цели"),
                    KeyboardButton(text="Изменить данные")
                ],
                [KeyboardButton(text=notify_text)],
                [KeyboardButton(text="Главная")]
            ]
    else:
        kbr = [
            [
                KeyboardButton(text="Изменить цели"),
                KeyboardButton(text="Изменить данные")
            ],
            [KeyboardButton(text=notify_text)],
            [KeyboardButton(text="Моя подписка")],
            [KeyboardButton(text="Главная")]
        ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kbr,
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def admin_exer():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Добавить упражнение в базу"), KeyboardButton(text="Создать тренировку")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def user_data():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Изменить возраст"), KeyboardButton(text="Изменить пол")],
            [KeyboardButton(text="Изменить рост"), KeyboardButton(text="Изменить вес")],
            [KeyboardButton(text="Изменить часовой пояс")],
            [KeyboardButton(text="Главная")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def ration():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [
                KeyboardButton(text="Изменить рацион"),
                KeyboardButton(text="Остaвить")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def train():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [
                KeyboardButton(text="Изменить тренировки"),
                KeyboardButton(text="Остaвить"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        )
    return keyboard


def weight_goal():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Да, изменить"), KeyboardButton(text="Нет")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True)
    return keyboard


def no():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text="Нет")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def food_book():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [KeyboardButton(text=" Просмотр приемов пищи за день")],
            [KeyboardButton(text=" Просмотр приемов пищи за неделю")],
            [KeyboardButton(text=" Трекер веса")],
            [KeyboardButton(text=" Главная")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True)
    return keyboard


def main_menu(is_admin=0, is_trainer=0):
    print(is_trainer)
    if is_trainer:
        main_kb = [
                [KeyboardButton(text="Меню управления тренера")],
                [KeyboardButton(text="Добавить приём пищи")],
                [KeyboardButton(text="Профиль"), KeyboardButton(text="Статистика")],
                [KeyboardButton(text="Замеры")]
            ]
    else:
        main_kb = [
                [KeyboardButton(text="Добавить приём пищи")],
                [KeyboardButton(text="Профиль"), KeyboardButton(text="Статистика")],
                [KeyboardButton(text="Замеры")]
            ]
    if is_admin:
        main_kb.append([KeyboardButton(text="Админпанель")])
    return ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)


def plans():
    plans_kb = ReplyKeyboardMarkup(keyboard=
    [
        [KeyboardButton(text="Рацион"), KeyboardButton(text="Тренировки")],
        [KeyboardButton(text="Главная")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True)
    return plans_kb


def gum():
    tren = ReplyKeyboardMarkup(keyboard=
    [
        [KeyboardButton(text="Главная")],
        [KeyboardButton(text="Тренировки")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True)
    return tren


def main():
    keyboard = ReplyKeyboardMarkup(keyboard=
    [
        [KeyboardButton(text="Главная")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True)
    return keyboard


def sex():
    keyboard = ReplyKeyboardMarkup(keyboard=
    [
        [KeyboardButton(text="М"), KeyboardButton(text="Ж")],
        [KeyboardButton(text="Главная")]
    ],
    resize_keyboard=True)
    return keyboard

def sport_lvl():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [
                KeyboardButton(text="1"),
                KeyboardButton(text="2"),
                KeyboardButton(text="3"),
                KeyboardButton(text="4")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard

def yes_no():
    keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [
                KeyboardButton(text="Да"),
                KeyboardButton(text="Нет")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard
