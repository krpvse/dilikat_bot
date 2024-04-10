from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from settings import settings


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=RedisStorage2(host=settings.REDIS_HOST, port=settings.REDIS_PORT))
