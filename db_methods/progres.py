import aiosqlite
from datetime import datetime
import pytz
from .conn import get_db_path

async def update_weight(user_id, weight):
    utc_now = datetime.now(pytz.utc)
    date = str(utc_now).replace(':', '.').split()[0]

    async with aiosqlite.connect(get_db_path()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM weight_data WHERE user_id = ? AND date = ?",
                (user_id, date)
            )
            data = await cursor.fetchall()

    print(data)
    
    if not data:
        print(1)
        async with aiosqlite.connect(get_db_path()) as db:
            await db.execute(
                "INSERT INTO weight_data (user_id, date, weight) VALUES (?, ?, ?)",
                (user_id, date, weight)
            )
            await db.commit()
    else:
        print(2)
        async with aiosqlite.connect(get_db_path()) as db:
            await db.execute(
                "UPDATE weight_data SET weight = ? WHERE user_id = ? AND date = ?",
                (weight, user_id, date)
            )
            await db.commit()

async def get_all_weight(user_id):
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM weight_data WHERE user_id = ? ORDER BY id DESC LIMIT 5;",
                (user_id,)
            )
            data = await cursor.fetchall()
    return data


async def get_weekly_weight(user_id):
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM weight_data 
                WHERE user_id = ? AND date >= date('now', '-7 days') 
                ORDER BY date DESC;
                """,
                (user_id,)
            )
            data = await cursor.fetchall()
    return data

async def get_monthly_weight(user_id):
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM weight_data 
                WHERE user_id = ? AND date >= date('now', '-30 days') 
                ORDER BY date DESC;
                """,
                (user_id,)
            )
            data = await cursor.fetchall()
    return data


async def get_quarter_weight(user_id):
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM weight_data 
                WHERE user_id = ? AND date >= date('now', '-90 days') 
                ORDER BY date DESC;
                """,
                (user_id,)
            )
            data = await cursor.fetchall()
    return data