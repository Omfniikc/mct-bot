import aiosqlite
import os
from datetime import datetime, timedelta
import pytz
from .conn import get_db_path

db_path = get_db_path()


async def get_food_data(food_id):
    async with aiosqlite.connect(db_path) as conn:
        food_data = await conn.execute(f"SELECT * FROM food_data WHERE id = ?", (food_id,))
        food_data = await food_data.fetchone()
        return food_data


async def correct_food_data(food_id, dishes, dishes_data):
    kcal = dishes_data["kcal"].replace(",", ".").replace("~", "").split(".")[0].split("-")[0]
    protein = dishes_data['p'].replace(",", ".").replace("~", "").split("-")[0]
    fat = dishes_data['f'].replace(",", ".").replace("~", "").split("-")[0]
    carbohydrate = dishes_data['c'].replace(",", ".").replace("~", "").split("-")[0]
    weight = dishes_data['weight'].replace(",", ".").replace("~", "").split(".")[0].split("-")[0]

    async with aiosqlite.connect(db_path) as conn:
        sql = '''
        UPDATE food_data SET kc = ?, protein = ?, fat = ?, carbohydrate = ?, weight = ? WHERE id = ?
        '''
        await conn.execute(sql, (kcal, protein, fat, carbohydrate, weight, food_id))

        for dish in dishes:
            await conn.execute(f"DELETE FROM dishes WHERE food_id = ?", (food_id,))
            await conn.execute(f"INSERT INTO dishes (food_id, dish) VALUES (?, ?)", (food_id, dish))

        await conn.commit()
        cur = await conn.cursor()

        food_data = await cur.execute(f"SELECT table_path FROM food_data WHERE id = ?", (food_id,))
        food_data = await food_data.fetchone()

        return food_data[0] if food_data else None


async def delete_food(food_id):
    async with aiosqlite.connect(db_path) as conn:
        cur = await conn.cursor()

        path_img = await cur.execute(f"SELECT table_path FROM food_data WHERE id = ?", (food_id,))
        path_img = await path_img.fetchone()

        if path_img:
            path_img = path_img[0]
            path_txt = path_img[:-4] + '.txt'

            if os.path.exists(path_img):
                os.remove(path_img)
            else:
                print(f"Файл {path_img} не найден.")
            
            if os.path.exists(path_txt):
                os.remove(path_txt)
            else:
                print(f"Файл {path_txt} не найден.")

            await cur.execute(f"DELETE FROM food_data WHERE id = ?", (food_id,))
            await conn.commit()

async def add_food_to_table(dishes, user_id, dishes_data, path, time, is_photo):
    kcal = dishes_data["kcal"]
    protein = dishes_data['p']
    fat = dishes_data['f']
    carbohydrate = dishes_data['c']
    weight = dishes_data['weight']
    async with aiosqlite.connect(db_path) as conn:
        print(dishes)
        sql = '''
        INSERT INTO food_data (user_id, table_path, kc, date, protein, fat, carbohydrate, weight, is_photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        await conn.execute(sql, (user_id, path, kcal, time, protein, fat, carbohydrate, weight, is_photo))
        await conn.commit()

        food_id = await conn.execute(f"SELECT id FROM food_data WHERE table_path = ?", (path,))
        food_id = await food_id.fetchone()

        if food_id:
            food_id = food_id[0]
            for dish in dishes:
                await conn.execute(f"INSERT INTO dishes (food_id, dish) VALUES (?, ?)", (food_id, dish))

            await conn.commit()
            return food_id

async def get_dishes(food_id):
    async with aiosqlite.connect(db_path) as conn:
        dishes = await conn.execute(f"SELECT dish FROM dishes WHERE food_id = ?", (food_id,))
        dishes = await dishes.fetchall()

        return dishes

async def food_check_daily(user_id, date=0, days=0):
    if date == 0:
        utc_now = datetime.now(pytz.utc) + timedelta(days=days)
        date = str(utc_now).split()[0]

    async with aiosqlite.connect(db_path) as conn:
        food = await conn.execute(f"SELECT * FROM food_data WHERE user_id = ? AND date = ?", (user_id, date))
        food = await food.fetchall()

        goals = await conn.execute(f"SELECT * FROM goals WHERE id = ?", (user_id,))
        goals = await goals.fetchone()

        return food, goals

async def update_last_food_time(user_id):
    now = datetime.utcnow()

    async with aiosqlite.connect(db_path) as conn:
        await conn.execute(f"UPDATE last_food SET last_time = ? WHERE user_id = ?", (now, user_id))
        await conn.commit()

async def get_last_food_time():
    async with aiosqlite.connect(db_path) as conn:
        data = await conn.execute(f"SELECT * FROM last_food")
        data = await data.fetchall()

        return data
