import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=str(os.getenv('SHOP_BOT_TOKEN')))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
