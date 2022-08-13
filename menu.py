
from aiogram.types import ReplyKeyboardMarkup
from config import BotDB

async def create_menu(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Статистика')

    return keyboard
