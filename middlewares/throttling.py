from aiogram import BaseMiddleware
import time


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.last_message = {}

    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        current_sec = time.time()
        if user_id in self.last_message and current_sec - self.last_message[user_id] < 1:
            return await event.answer("Не спамь")
        else:
            self.last_message[user_id] = current_sec
            return await handler(event, data)


