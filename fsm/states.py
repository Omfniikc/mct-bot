from aiogram.fsm.state import State, StatesGroup
import numpy as np


class correct_food(StatesGroup):
    comment = State()
    delete = State()


class ration_form(StatesGroup):
    age = State()
    sex = State()
    height = State()
    weight = State()
    goal = State()
    food_cancel = State()
    sport_lvl = State()
    eat_count = State()
    comment = State()


class Form_tren(StatesGroup):
    k1 = State()
    k2 = State()
    k3 = State()
    k4 = State()
    k5 = State()
    k6 = State()
    k7 = State()
    k8 = State()
    k9 = State()


class Ration():
    ration = {}
    tren = {}


class goals(StatesGroup):
    set_menu = State()
    kcal = State()
    protein = State()
    fat = State()
    carbohydrate = State()
    weight = State()


class DailyFood(StatesGroup):
    p1 = {}
    p2 = {}
    p3 = {}
    p4 = {}
    p5 = {}
    p6 = {}
    p7 = {}


class Statistics(StatesGroup):
    data_arr = []
    arr = []
    weight = State()
    np_data_arr = np.array(data_arr)
    np_arr = np.array(arr)


class Food_edit(StatesGroup):
    k = State()


class main_menu(StatesGroup):
    add_food = State()
    profile = State()
    food_note = State()
    plans = State()
    progres = State()
    start = State()
    start_user = State()
    user_name = State()
    user_surname = State()

class measurements(StatesGroup):
    menu = State()
    weight = State()
    add_weight = State()
    figure = State()
    power = State()
    add_power = State()
    power_stat =State()
    add_figure = State()
    figure_stat = State()


class progres(StatesGroup):
    set_weight = State()


class user_data(StatesGroup):
    menu = State()
    set_time = State()
    set_age = State()
    set_sex = State()
    set_weight = State()
    set_height = State()
    email = State()

class trens(StatesGroup):
    tren = State()

class admin_tren(StatesGroup):
    name = State()
    desc = State()
    times = State()
    exers = State()

class admin_exer(StatesGroup):
    name = State()
    mini_desc = State()
    desc = State()
    photo = State()
    video = State()
    submit = State()

class newslater(StatesGroup):
    message = State()
    ready = State()
    point_message = State()
    point_users = State()
    point_ready = State()


class admin_panel(StatesGroup):
    referral_statistics = State()
    add_trainer = State()
    get_photo = State()
    add_sub = State()
    delete_user = State()
    upload_db = State()
    referral_statistics = State()
    add_admin = State()
    get_photo = State()
    add_sub = State()
    sql_query = State()

class trainer_panel(StatesGroup):
    main_menu = State()
    choose_user_statistic = State()
    set_date_users = State()
    users_statistic = State()
    user_goals = State()
    goal_kcal = State()
    goal_protein = State()
    goal_fat = State()
    goal_carbohydrate = State()
    delete_user = State()
    delete_user_accept = State()
    set_day_user = State()
    set_date_user = State()
    choose_user_food = State()
    choose_user_measurements = State()
    user_measurements_stat = State()
    choose_user_measurements_stat = State()
    measurements_power = State()
    measurements_figure = State()
    measurements_figure_l = State()
    measurements_weight = State()


class WeightStates(StatesGroup):
    set_weight = State()
    week = State()
    month = State()
    quarter = State()

class SubscriptionStates(StatesGroup):
    sub = State()
    confirm_cancel = State()
    feedback = State()