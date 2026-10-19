from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class PrivateChatMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            chat = event.chat
            if chat.type in {"group", "supergroup"}:
                # Останавливаем обработку, если это группа или супергруппа
                return
        # Продолжаем обработку для личных сообщений
        return await handler(event, data)

