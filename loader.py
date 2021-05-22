import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=str(os.getenv('API_TOKEN_BOT')))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
