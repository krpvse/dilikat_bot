from aioredis import Redis
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine

from config import bot_token, db_host, db_port, db_name, db_user, db_password, redis_host, redis_port


db_engine = create_async_engine(f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
redis = Redis(host=redis_host, port=redis_port, decode_responses=True)

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=RedisStorage2(host=redis_host, port=redis_port))
