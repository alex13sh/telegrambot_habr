from aiogram import types
from misc import dp

from db import Base, Session
from db import Column, Integer, String, Boolean, DateTime
import datetime

class BD_Users(Base):
    __tablename__ = 'BD_Users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255))
    time_start = Column(DateTime()) 
    time_last = Column(DateTime()) 
    
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

kb_start_1 = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row('/subscribe', '/unsubscribe', '/list_sub')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)\
        .row('Подписаться', 'Отписаться')\
        .add('Список подписок')

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
            , reply_markup=kb_start) 

    user_id = message.from_user.id
    print("from_user:", message.from_user)
    try:
        session = Session()
        session.add(BD_Users(
            user_id     = message.from_user.id,
            user_name   = message.from_user.username,
            time_start  = datetime.datetime.now(),
            time_last   = datetime.datetime.now()
        ))
        session.commit()
    except:
        session.rollback()
        print("Пользователь уже был добавлен")
