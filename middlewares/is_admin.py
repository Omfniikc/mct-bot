from aiogram import Bot, Dispatcher, types, F, BaseMiddleware

from keyboards import reply as kbr
from keyboards import inline as kbi
from db_methods.user_methods import is_admin


class AdminFilter(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data):
        user_id = event.from_user.id

        is_a = await is_admin(user_id)
        if is_a:
            return await handler(event, data)

        