from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp
#from parser.stopgame import StopGame
from db import Base, Session
from db import Column, Integer, String

class BD_Subs(Base):
    __tablename__ = 'BD_Subs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sub_name = Column(String(255)) 
    
class OrderSubs(StatesGroup):
    waiting_for_select_website = State()
    waiting_for_subs_name = State()
    
# Команда активации подписки
@dp.message_handler(commands='subscribe', state='*')
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
        await message.answer("На кого хотите подписаться? Укажите имя:")
    elif website == "StopGame":
        await state.finish()
        session = Session()
        session.add(BD_Subs(user_id=message.from_user.id, sub_name=f"{website}"))
        session.commit()
        await message.answer(f"Вы успешно подписались на рассылку! На сайт {website}")
    
@dp.message_handler(state=OrderSubs.waiting_for_subs_name, content_types=types.ContentTypes.TEXT)
async def subscribe_name(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    data = await state.get_data()
    website = data["website"]
    name = message.text
    session = Session()
    session.add(BD_Subs(user_id=message.from_user.id, sub_name=f"{website}_{name}"))
    session.commit()
    await message.answer(f"Вы успешно подписались на рассылку! На сайт {website} По имени: {name}")
    await state.finish()
    
# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    session = Session()
    txt = ""
    for (sub_name,) in session.query(BD_Subs.sub_name).filter_by(user_id=message.from_user.id): 
        txt += "\n" + str(sub_name)
    await message.answer("Вы успешно отписаны от рассылки сайта:" + txt)
    q = session.query(BD_Subs).filter(BD_Subs.user_id == message.from_user.id)\
    .delete()
    session.commit()
    await message.reply("Ну и ладно!")
