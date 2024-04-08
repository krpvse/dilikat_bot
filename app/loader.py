from aioredis import Redis
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine

from settings import settings


db_engine = create_async_engine(settings.DATABASE_URL)
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=RedisStorage2(host=settings.REDIS_HOST, port=settings.REDIS_PORT))
