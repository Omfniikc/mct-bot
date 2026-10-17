import asyncio
import ssl

import certifi
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import sys
import logging

from handlers import (
    pay,
    admin, 
    start, 
    main_menu,
    add_food,
    corect_food,
    profile,
    goals,
    ration,
    food_note,
    trash,
    progres,
    send_notify,
    trainers_menu,
    time,
    measurements
    )

from config import *


def create_bot() -> Bot:
    """Создаёт Bot, используя прокси из PROXY_URL (если задан)."""
    if PROXY_URL:
        session = AiohttpSession(proxy=PROXY_URL)
        # Баг aiogram: при включении прокси ssl-контекст теряется из настроек
        # коннектора, и aiohttp падает на системное хранилище сертификатов
        # Windows, которое не принимает MITM-сертификат прокси (Hiddify).
        # Возвращаем certifi явно — тот же пучок CA, что aiogram использует
        # в режиме без прокси.
        session._connector_init["ssl"] = ssl.create_default_context(cafile=certifi.where())
        return Bot(token=TG_TOKEN, session=session)
    return Bot(token=TG_TOKEN)


async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

    asyncio.create_task(send_notify.start_scheduler_notify())
    asyncio.create_task(pay.start_scheduler_sub())
    asyncio.create_task(food_note.stat())
    asyncio.create_task(trainers_menu.trainers_stat())

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

async def main():
    bot = create_bot()
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        main_menu.router,
        send_notify.router,
        measurements.router,
        admin.router,
        pay.router,
        trainers_menu.router,
        progres.router,
        profile.router,
        corect_food.router,
        goals.router,
        ration.router,
        food_note.router,
        add_food.router,  
        add_food.all_router,       
        time.router,
        trash.router
        )
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()

    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)

    webhook_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    return app

async def mainpoling():
    bot = create_bot()
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        main_menu.router,
        send_notify.router,
        measurements.router,
        admin.router,
        pay.router,
        trainers_menu.router,
        progres.router,
        profile.router,
        corect_food.router,
        goals.router,
        ration.router,
        food_note.router,
        add_food.router,  
        add_food.all_router,       
        time.router,
        trash.router
        )
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    await send_notify.start_scheduler_notify()
    await pay.start_scheduler_sub()
    await food_note.stat()
    await trainers_menu.trainers_stat()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG if POLING else logging.WARNING,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)20s:%(lineno)-3d %(levelname)-8s - %(message)s",
        )

    if POLING:
        asyncio.run(mainpoling())
    else:
        web.run_app(
            asyncio.run(main()),
            host="localhost",
            port=WEBHOOK_PORT
        )
