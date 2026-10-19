from aiogram import Bot, Dispatcher, types, F, BaseMiddleware

from keyboards import reply as kbr
from keyboards import inline as kbi
from db_methods.user_methods import is_subscription
from text.messages import *
from config import *


bot = Bot(token=TG_TOKEN)

class HasSubscriptionFilter(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data):
        user_id = event.from_user.id

        subscription_data = await is_subscription(user_id)
        print(len(subscription_data))
        if subscription_data[0] != "1":
            if len(subscription_data) == 1:
                await event.answer(BOT_INACTIVE_MESSAGES[0])
                await event.answer(BOT_INACTIVE_MESSAGES[1], reply_markup=kbi.choose_pay())
            elif len(subscription_data) == 2:
                await event.answer(BOT_INACTIVE_MESSAGES[2], relpy_markup=kbi.main())
                await bot.send_message(subscription_data[1], "Ваши клиенты пытаются воспользоваться ботом, но у вас не активна подписка")
                await bot.send_message(subscription_data[1], BOT_INACTIVE_MESSAGES[1], reply_markup=kbi.choose_pay())
            return
        
        # Передаем данные дальше по цепочке
        return await handler(event, data)