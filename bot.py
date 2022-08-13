from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from functions import registration_user, get_stats, check_tokens_price
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import dp

scheduler = AsyncIOScheduler()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    
    await registration_user(message, message.from_user.id)

@dp.message_handler(Text(equals='Статистика'))
async def stats(message: types.Message):
    
    await get_stats(message)

        
if __name__ == '__main__':
    scheduler.add_job(check_tokens_price, "interval", seconds=30)
    scheduler.start()
    executor.start_polling(dp)