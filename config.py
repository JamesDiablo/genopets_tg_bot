from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import BotDB


bot = Bot(token='token')
dp = Dispatcher(bot, storage = MemoryStorage())
BotDB = BotDB('db.db')
