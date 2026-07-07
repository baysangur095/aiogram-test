from aiogram import Bot, Dispatcher
from database.models import create_table
from handlers.start import start_router
from handlers.notes import notes_router
import config
import asyncio
from aiogram.fsm.storage.redis import RedisStorage
from middlewares.throttling import ThrottlingMiddleware

bot = Bot(token=config.BOT_TOKEN)

storage = RedisStorage.from_url("redis://localhost:6379/0")
dp = Dispatcher(storage=storage)

dp.include_routers(start_router, notes_router)

async def on_startup():
    await create_table()


dp.startup.register(on_startup)
dp.message.outer_middleware(ThrottlingMiddleware())




if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))