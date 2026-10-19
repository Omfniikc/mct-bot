import aiosqlite
from .conn import get_db_path

db_path = get_db_path()

async def get_path(food_id):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cur:
            # Параметризованный запрос для защиты от SQL-инъекций
            await cur.execute("SELECT table_path FROM food_data WHERE id = ?", (food_id,))
            result = await cur.fetchone()
            
            if result:
                path_img = result[0][:-4]
                return path_img
            else:
                return None
