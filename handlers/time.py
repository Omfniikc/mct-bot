from aiogram import Router, F
from aiogram.types import CallbackQuery

from middlewares.is_group import PrivateChatMiddleware
from db_methods.user_methods import add_GMT
from keyboards import inline as kbi

from datetime import datetime, timedelta


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.callback_query(F.data[:5] == "time_")
async def set_time(callback: CallbackQuery):
    time = callback.data.split('_')[1]
    utc_now = int(str(datetime.utcnow()).split()[1].split(":")[0])
    print(utc_now)
    offset = int(str(timedelta(hours=int(time))).split(':')[0])
    s = offset-utc_now
    print(s)
    await add_GMT(callback.from_user.id, s)
    await callback.message.edit_text("Время задано", reply_markup=kbi.main())
