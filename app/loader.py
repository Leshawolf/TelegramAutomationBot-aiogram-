import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiomysql

import app.config as cfg

bot = Bot(
    token=cfg.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
)

storage = MemoryStorage()

dp = Dispatcher(
    bot=bot,
    storage=storage,
)


async def create_connection_pool(loop):
    pool = await aiomysql.create_pool(
        host=cfg.HOST,
        user=cfg.USER,
        password=cfg.PASS,
        db=cfg.DATABASE,
        loop=loop,
        autocommit=True
    )
    return pool

storage = MemoryStorage()
loop = asyncio.get_event_loop()
MYSQL_POOL = loop.run_until_complete(create_connection_pool(loop))


__all__ = (
    "bot",
    "storage",
    "dp",
)