from aiogram import types
from misc import dp

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('/subscribe')
       , KeyboardButton('/unsubscribe'))

from . import subs

# Команда активации подписки
@dp.message_handler(commands=['start'])
async def start(message: types.Message):  
    argument = message.get_args()
    if argument: 
        message.text = argument
        #await message.answer("Реферальный текст: "+message.text)
        if message.text[0] == "_":
            if message.text.startswith("_subscribe"):
                message.text = "/" + message.text[1:10] + " " + message.text[11:]
                await subs.subscribe(message)
    else:
        await message.answer("Добро пожаловать в тестовый бот для Habr и StopGame"
            , reply_markup=start_kb) 
