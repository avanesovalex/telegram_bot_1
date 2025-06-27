import asyncio
from aiogram import Dispatcher, Bot

from src.config import config
from src.database.db import db
from src.handlers import registration, admin
from src.files import commands


bot = Bot(token=config.TOKEN)
dp = Dispatcher()

dp.include_router(registration.router)
dp.include_router(admin.router)


@dp.startup()
async def on_startup():
    await db.connect()
    await commands.set_commands(bot)


@dp.shutdown()
async def on_shutdown():
    await db.close()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
