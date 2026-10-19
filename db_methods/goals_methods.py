import aiosqlite
from .conn import get_db_path

db_path = get_db_path()

async def get_user_goal(user_id):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "SELECT * FROM goals WHERE id = ?"
            results = await cur.execute(sql, (user_id,))
            results = await results.fetchone()
            return results

async def add_ration(ans, user_id, k, p, f, c):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = '''
            UPDATE goals 
            SET kcal = ?, protein = ?, fat = ?, carbohydrate = ?, ration = ?
            WHERE id = ?
            '''
            await cur.execute(sql, (k, p, f, c, ans, user_id))
            await conn.commit()

async def get_tren(user_id):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "SELECT train FROM goals WHERE id = ?"
            result = await cur.execute(sql, (user_id,))
            result = await result.fetchone()
            train = result[0]
            if train is None:
                return [0, 0]
            else:
                return [1, train]

async def update_kcal(user_id, kcal):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET kcal = ? WHERE id = ?"
            await cur.execute(sql, (kcal, user_id))
            await conn.commit()

async def update_protein(user_id, protein):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET protein = ? WHERE id = ?"
            await cur.execute(sql, (protein, user_id))
            await conn.commit()

async def update_fat(user_id, fat):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET fat = ? WHERE id = ?"
            await cur.execute(sql, (fat, user_id))
            await conn.commit()

async def update_carbohydrate(user_id, carbohydrate):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET carbohydrate = ? WHERE id = ?"
            await cur.execute(sql, (carbohydrate, user_id))
            await conn.commit()

async def update_weight(user_id, weight):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET weight = ? WHERE id = ?"
            await cur.execute(sql, (weight, user_id))
            await conn.commit()

async def update_goals(user_id, kcal=0, protein=0, fat=0, carbohydrate=0, weight=0, ration=None, train=None):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = '''
            UPDATE goals 
            SET kcal = ?, protein = ?, fat = ?, carbohydrate = ?, weight = ?, ration = ?, train = ?
            WHERE id = ?
            '''
            await cur.execute(sql, (kcal, protein, fat, carbohydrate, weight, ration, train, user_id))
            await conn.commit()

async def add_tren(ans, user_id):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET train = ? WHERE id = ?"
            await cur.execute(sql, (ans, user_id))
            await conn.commit()

async def add_goal_kcal(goal, user_id):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET kcal = ? WHERE id = ?"
            await cur.execute(sql, (goal, user_id))
            await conn.commit()

async def add_goal_weight(text, user_id):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE goals SET weight = ? WHERE id = ?"
            await cur.execute(sql, (text, user_id))
            await conn.commit()
