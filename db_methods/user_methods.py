import aiosqlite
from datetime import datetime, timedelta

import pytz

from db_methods.conn import get_db_path
from fsm.states import user_data

db_path = get_db_path()


async def set_user_name(name, surname, user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET name = ?, surname = ? WHERE user_id = ?", (name, surname, user_id))
        await db.commit()

async def get_user_email(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT email FROM user_info WHERE user_id = ?", (user_id,))
            results = await cursor.fetchone()
    return results

async def set_email(email, user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET email = ? WHERE user_id = ?", (email, user_id))
        await db.commit()

async def is_admin(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            is_a = await cursor.execute("SELECT * FROM admins WHERE user_id = {}".format(user_id,))
            if await is_a.fetchone() is None:
                return False
            return True

async def is_trainer(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            is_t = await cursor.execute("SELECT * FROM trainers WHERE user_id = {}".format(user_id,))
            if await is_t.fetchone() is None:
                return False
            return True

async def add_user(user_id, username):
    today_utc = datetime.utcnow().date()

    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            info_user_to = await cursor.execute("SELECT * FROM goals WHERE id = ?", (user_id,))
            if await info_user_to.fetchone() is None:
                await cursor.execute("INSERT INTO goals (id) VALUES (?)", (user_id,))
            
            info_user_to_all = await cursor.execute("SELECT * FROM user_info WHERE user_id = ?", (user_id,))
            if await info_user_to_all.fetchone() is None:
                await cursor.execute("INSERT INTO user_info (user_id, username) VALUES (?, ?)", (user_id, username,))
            
            info_user_time = await cursor.execute("SELECT * FROM last_food WHERE user_id = ?", (user_id,))
            if await info_user_time.fetchone() is None:
                await cursor.execute("INSERT INTO last_food (user_id) VALUES (?)", (user_id,))

        await db.commit()

async def add_GMT(user_id, time):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "UPDATE last_food SET breakfast_time = ?, lunch_time = ?, dinner_time = ? WHERE user_id = ?",
            (8 - time, 13 - time, 18 - time, user_id)
        )
        await db.execute(
            "UPDATE user_info SET time = ? WHERE user_id = ?",
            (time, user_id)
        )
        await db.commit()

async def get_user_info(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM user_info WHERE user_id = ?", (user_id,))
            results = await cursor.fetchone()
    return results

async def add_weight(w, user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET weight = ? WHERE user_id = ?", (w, user_id))
        await db.commit()

async def add_age(a, user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET age = ? WHERE user_id = ?", (a, user_id))
        await db.commit()

async def add_height(h, user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET height = ? WHERE user_id = ?", (h, user_id))
        await db.commit()

async def set_notification(user_id, data):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE last_food SET is_notify = ? WHERE user_id = ?", (data, user_id))
        await db.commit()

async def add_sex(s, user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET sex = ? WHERE user_id = ?", (s, user_id))
        await db.commit()

async def get_all_user_id():
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT user_id FROM user_info")
            usr_ids = await cursor.fetchall()
    return [int(x[0]) for x in usr_ids]

async def user_is_notify(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT is_notify FROM last_food WHERE user_id = ?", (user_id,))
            is_notify = await cursor.fetchone()
    return int(is_notify[0])


async def off_subscription(user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE trainers SET is_active = 0 WHERE user_id = ?", (user_id,))
        await db.commit()

async def get_all_subscription():
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM trainers")
            data = await cursor.fetchall()
            print(data)
    return data

async def is_subscription(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT is_active, user_id FROM trainers WHERE user_id = (SELECT trainer_id FROM user_info WHERE user_id = {})".format(user_id))
            data = await cursor.fetchone()
            if data is None:
                await cursor.execute("SELECT is_active FROM trainers WHERE user_id = {user_id}".format(user_id=user_id))
                data = await cursor.fetchone()
            print(data)
    return data

async def add_admin(user_id):
    print(user_id)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT into admins (user_id) VALUES ({})".format(user_id))
            
        await db.commit()

async def add_trainer(user_id, sub_days):
    today_utc = datetime.utcnow().date()
    last_date = str(today_utc + timedelta(days=int(sub_days)))
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM trainers WHERE user_id = {user_id}".format(user_id=user_id))
            data = await cursor.fetchone()
        if data is None:
            await db.execute('INSERT into trainers (user_id, is_active, last_day) VALUES (?, 1, ?)', (user_id, last_date))
        else:
            await db.execute("UPDATE trainers SET last_day = ?, is_active = 1 WHERE user_id = ?", (last_date, user_id))

        await db.commit()

async def add_subscription(user_id, days):
    today_utc = datetime.utcnow().date()
    last_date = today_utc + timedelta(days=days)
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "UPDATE trainers SET is_active = 1, last_day = ? WHERE user_id = ?",
            (last_date, user_id)
        )
        await db.commit()

async def add_trainer_for_user(user_id, trainer_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET trainer_id = {} WHERE user_id = {}".format(trainer_id, user_id))

        await db.commit()

    

async def add_ref(user_id, host_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT into refs (user_id, is_activated, host_id) VALUES ({}, {}, {})".format(user_id, 0, host_id))
            
        await db.commit()

async def is_ref(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM refs WHERE `user_id` = {}".format(user_id))
            data = await cursor.fetchone()

    return data

async def activate_ref(user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE refs SET is_activated = 1 WHERE user_id = {}".format(user_id))
        await db.commit()

async def get_referral_statistics(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            sql = "SELECT user_id FROM refs WHERE host_id = ? AND is_activated = 1"
            await cur.execute(sql, (user_id,))
            data = await cur.fetchall()
    return data

async def get_trainers_user_statistic(user_id, days=0, date=0):
    if date == 0:
        utc_now = datetime.now(pytz.utc) + timedelta(days=days)
        date = str(utc_now).split()[0]
    sql = '''
SELECT 
    user_info.user_id,
    food_data.kc,
    food_data.protein,
    food_data.fat,
    food_data.carbohydrate,
    goals.kcal,
    goals.protein,
    goals.fat,
    goals.carbohydrate,
    user_info.name,
    user_info.surname
FROM 
    user_info
JOIN 
    goals
ON 
    user_info.user_id = goals.id
LEFT JOIN 
    food_data
ON 
    user_info.user_id = food_data.user_id
    AND food_data.date = "{date}"
WHERE 
    user_info.trainer_id = {user_id};
'''
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            await cur.execute(sql.format(user_id=user_id, date=date))
            data = await cur.fetchall()
    cal = {}
    prot = {}
    fat = {}
    car = {}
    goals = {}
    names = {}
    for i in data:
        print(i)
        k = 0 if i[1] is None else int(i[1])
        p = 0 if i[2] is None else float(i[2])
        f = 0 if i[3] is None else float(i[3])
        c = 0 if i[4] is None else float(i[4])
        if i[0] in cal:
            cal[i[0]] += k
        else:
            cal[i[0]] = k
        if i[0] in prot:
            prot[i[0]] += p
        else:
            prot[i[0]] = p
        if i[0] in fat:
            fat[i[0]] += f
        else:
            fat[i[0]] = f
        if i[0] in car:
            car[i[0]] += c
        else:
            car[i[0]] = c
        goals[i[0]] = [i[5], i[6], i[7], i[8]]
        name = i[9] + " " + i[10] if i[9] and i[10] else i[9] if i[9] else i[10]
        names[i[0]] = name
    data_out = []
    for i in cal:
        user_d = [i, cal[i], prot[i], fat[i], car[i], goals[i][0], goals[i][1], goals[i][2], goals[i][3], names[i]]
        data_out.append(user_d)

    return data_out

async def get_trainer_users(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            sql = "SELECT user_id FROM user_info WHERE trainer_id = {}".format(user_id)
            await cur.execute(sql)
            data = await cur.fetchone()
    return data

async def get_trainer_user(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            sql = "SELECT user_id, name, surname FROM user_info WHERE trainer_id = {}".format(user_id)
            await cur.execute(sql)
            data = await cur.fetchall()
    return data

async def delete_user_from_trainer(user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE user_info SET trainer_id = NULL WHERE user_id = ?", (user_id,))
        await db.commit()


async def add_measurements_power(user_id, exercise, weight, count):
    today = datetime.now().strftime("%d.%m.%y")
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT INTO exercises (user_id, exercise, date, weight, count) VALUES (?, ?, ?, ?, ?)", (user_id, exercise, today, weight, count))
        await db.commit()


async def add_measurements_figure(user_id, name, value):
    today = datetime.now().strftime("%d.%m.%y")
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT INTO figure (user_id, name, date, value) VALUES (?, ?, ?, ?)", (user_id, name, today, value))
        await db.commit()

async def get_measurements_power(user_id, exercise):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            sql = "SELECT * FROM exercises WHERE user_id = ? AND exercise = ?"
            await cur.execute(sql, (user_id, exercise))
            data = await cur.fetchall()
    return data

async def get_measurements_figure(user_id, name):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            sql = "SELECT * FROM figure WHERE user_id = ? AND name = ?"
            await cur.execute(sql, (user_id, name))
            data = await cur.fetchall()
    return data

async def get_all_measurements(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cur:
            sql = "SELECT * FROM figure WHERE user_id = ? AND name = ?"
            await cur.execute(sql, (user_id))
            data = await cur.fetchall()
    return data

    
async def get_all_measurements(user_id):
    async with aiosqlite.connect(db_path) as db:
        # Получение последних замеров фигуры
        figure_data = {}
        async with db.cursor() as cur:
            sql_figure = """
            SELECT f.name, f.date, f.value
            FROM figure f
            WHERE user_id = ? AND date = (
                SELECT MAX(date) 
                FROM figure 
                WHERE user_id = ? AND name = f.name
            )
            GROUP BY f.name
            """
            await cur.execute(sql_figure, (user_id, user_id))
            rows = await cur.fetchall()
            for row in rows:
                figure_data[row[0]] = {"date": row[1], "value": row[2]}
        
        # Получение последних замеров упражнений
        exercise_data = {}
        async with db.cursor() as cur:
            sql_exercise = """
            SELECT e.exercise, e.date, e.weight, e.count
            FROM exercises e
            WHERE user_id = ? AND date = (
                SELECT MAX(date) 
                FROM exercises 
                WHERE user_id = ? AND exercise = e.exercise
            )
            GROUP BY e.exercise
            """
            await cur.execute(sql_exercise, (user_id, user_id))
            rows = await cur.fetchall()
            for row in rows:
                exercise_data[row[0]] = {"date": row[1], "weight": row[2], "count": row[3]}
        
        return {
            "figure": figure_data,
            "exercises": exercise_data
        }
    
async def save_user_payment(user_id, payment):
    async with aiosqlite.connect(db_path) as db:
        sql = "select * from payments where user_id = ?"
        async with db.cursor() as cursor:
            await cursor.execute(sql, (user_id, ))
            data = await cursor.fetchone()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if data is None:
            sql = "insert into payments (user_id, payment, date) values (?, ?, ?)"
            await db.execute(sql, (user_id, payment, date))
        else:
            sql = "update payments set payment = ?, date = ? where user_id = ?"
            await db.execute(sql, (payment, date, user_id))
        await db.commit()

async def change_sub_not(user_id, status):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "UPDATE trainers SET back_to_sub = ? WHERE user_id = ?",
            (status, user_id)
        )
        await db.commit()

async def save_user_consent(user_id, consent):
    async with aiosqlite.connect(db_path) as db:
        sql = "select * from is_autopay where user_id = ?"
        async with db.cursor() as cursor:
            await cursor.execute(sql, (user_id, ))
            data = await cursor.fetchone()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if data is None:
            sql = "insert into is_autopay (user_id, is_accept, date) values (?, ?, ?)"
            await db.execute(sql, (user_id, consent, date))
        else:
            sql = "update is_autopay set is_accept = ?, date = ? where user_id = ?"
            await db.execute(sql, (consent, date, user_id))
        await db.commit()
        

async def get_user_consent(user_id):
    async with aiosqlite.connect(db_path) as db:
        sql = "select * from is_autopay where user_id = ?"
        async with db.cursor() as cursor:
            await cursor.execute(sql, (user_id, ))
            data = await cursor.fetchone()
    return data

async def get_user_payment(user_id):
    async with aiosqlite.connect(db_path) as db:
        sql = "select * from payments where user_id = ?"
        async with db.cursor() as cursor:
            await cursor.execute(sql, (user_id, ))
            data = await cursor.fetchone()
    return data

async def get_subscription(user_id):
    async with aiosqlite.connect(db_path) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM trainers WHERE user_id = ?", (user_id,))
            data = await cursor.fetchone()
    return data

async def do_sql(sql):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(sql)
        await db.commit()