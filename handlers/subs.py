from aiogram import types
from aiogram.dispatcher import FSMContext
from misc import dp, bot
#from parser.stopgame import StopGame
from db import Base, Session
from db import Column, Integer, String
from . import kb as start

class BD_Subs(Base):
    __tablename__ = 'BD_Subs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sub_name = Column(String(255))
    #sms_id = Column(Integer)
    
class BD_Subs_SMS(Base):
    __tablename__ = 'BD_Subs_SMS'
    sms_id = Column(Integer, primary_key=True)
    subs_id = Column(Integer)
    
def new_subs(user_id, sub_name, sms_id=None):
    session = Session()
    row = BD_Subs(user_id=user_id, sub_name=sub_name)
    session.add(row)
    session.commit()
    #session.refresh(row)
    if sms_id:
        session.add(BD_Subs_SMS(sms_id=sms_id, subs_id=row.id))
        session.commit()
    
from aiogram.dispatcher.filters.state import State, StatesGroup
class OrderSubs(StatesGroup):
    waiting_for_select_website = State()
    waiting_for_subs_name = State()
    
# Команда активации подписки
@dp.message_handler(commands='subscribe', state='*')
@dp.message_handler(lambda message: message.text == "Подписаться", content_types=types.ContentTypes.TEXT)
async def subscribe(message: types.Message):
    argument = message.get_args()
    if argument:
        name = argument
        await message.answer("Вы успешно подписались на рассылку! По имени: "+name)
    else:
        await OrderSubs.waiting_for_select_website.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Habr", "StopGame")
        await message.answer("На кого хотите подписаться? Выберите сайт:", reply_markup=keyboard)

@dp.message_handler(state=OrderSubs.waiting_for_select_website, content_types=types.ContentTypes.TEXT)
async def subscribe_website(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    website = message.text
    if website == "Habr":
        await state.update_data(website=website)
        await OrderSubs.next()
        await message.answer("На кого хотите подписаться? Укажите имя:", reply_markup=start.ReplyKeyboardRemove())
    elif website == "StopGame":
        await state.finish()
        new_subs(user_id=message.from_user.id, sub_name=f"{website}")
        await message.answer(f"Вы успешно подписались на рассылку! На сайт {website}", reply_markup=start.kb_start)
    else:
        await message.answer("Выберите комманду!")
    
@dp.message_handler(state=OrderSubs.waiting_for_subs_name, content_types=types.ContentTypes.TEXT)
async def subscribe_name(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    data = await state.get_data()
    website = data["website"]
    name = message.text
    sms = await message.answer(f"Вы успешно подписались на рассылку! На сайт {website} По имени: {name}", reply_markup=start.kb_start)
    new_subs(
        user_id=message.from_user.id, 
        sub_name=f"{website}_{name}",
        sms_id = sms["message_id"]
    )
    await state.finish()
 
# message.get_args()
def filter_start_subs(message):
    args = message.get_args()
    if args and args.startswith("_subscribe="):
        message.text = args[11:]
        return True
    else: return False

@dp.message_handler(filter_start_subs, commands=['start']) #, text_startswith="start _subscribe=")
async def subscribe_new(message: types.Message):  # обратите внимание, есть второй аргумент
    website = message.text
    new_subs(user_id=message.from_user.id, sub_name=f"{website}")
    await message.answer(f"Вы успешно подписались на рассылку! На сайт {website}", reply_markup=start.kb_start)

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
@dp.message_handler(lambda message: message.text == "Отписаться", content_types=types.ContentTypes.TEXT)
async def unsubscribe(message: types.Message):
    session = Session()
    if "reply_to_message" in message:
        res = session.query(BD_Subs_SMS).filter_by(sms_id=message["reply_to_message"]["message_id"]).all()
        if len(res) > 0:
            row_1 = res[0]
            print("Result subs_id:", row_1.subs_id)
            row_2 = session.query(BD_Subs).filter_by(id=row_1.subs_id).all()[0]
            await message.answer("Удалил подписку: "+row_2.sub_name)
            session.delete(row_2)
            session.delete(row_1)
        else:
            await message.answer("Я не нашёл подписку")
    else:
        txt = ""
        for (sub_name,) in session.query(BD_Subs.sub_name).filter_by(user_id=message.from_user.id): 
            txt += "\n" + str(sub_name)
        await message.answer("Вы успешно отписаны от рассылки сайта:" + txt)
        q = session.query(BD_Subs).filter(BD_Subs.user_id == message.from_user.id)\
        .delete()
        session.commit()
        await message.reply("Ну и ладно!")

@dp.message_handler(commands=['list_sub'])
@dp.message_handler(lambda message: message.text == "Список подписок", content_types=types.ContentTypes.TEXT)
async def list_sub(message: types.Message):
    session = Session()
    txt = ""
    for (sub_name,) in session.query(BD_Subs.sub_name).filter_by(user_id=message.from_user.id): 
        txt += "\n" + str(sub_name)
    inline_kb = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            'Посмотреть список!', 
            switch_inline_query_current_chat='#subs'
        ))
    await message.answer("Список ваших подписок:" + txt, reply_markup=inline_kb)
    
    
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
import hashlib

def filter_query_subs(query):
    if query.query.startswith("#subs"):
        query.query = query.query[6:].lower()
        return True
    else: return False

@dp.inline_handler(filter_query_subs)
async def list_sub(inline_query: InlineQuery):
    session = Session()
    _startwith = inline_query.query
    items = []
    for row in session.query(BD_Subs).filter_by(user_id=inline_query.from_user.id):
        if not row.sub_name.lower().startswith(_startwith): continue
        
        sub_name = row.sub_name
        item = InlineQueryResultArticle(
            id=row.id,
            title=f'Result {sub_name}',
            input_message_content=InputTextMessageContent(sub_name),
        )
        items.append(item)
        
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)
