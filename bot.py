import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types


# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


# Команда активации подписки
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):	
    await message.answer("Добро пожаловать в тестовый бот для Habr и StopGame")

# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):	
    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    await message.answer("Вы успешно отписаны от рассылки.")


# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
