from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp

class OrderSubs(StatesGroup):
    waiting_for_subs_name = State()
    #waiting_for_food_size = State()
    
# Команда активации подписки
@dp.message_handler(commands='subscribe', state='*')
async def subscribe(message: types.Message):
    name = None
    if len(message.text) > 10:
        name = message.text[11:]
    if name: 
        await message.answer("Вы успешно подписались на рассылку! По имени: "+name)
    else:
        await message.answer("На кого хотите подписаться? Укажите имя:")
        await OrderSubs.waiting_for_subs_name.set()

@dp.message_handler(state=OrderSubs.waiting_for_subs_name, content_types=types.ContentTypes.TEXT)
async def subscribe_name(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    name = message.text
    await message.answer("Вы успешно подписались на рассылку! По имени: "+name)
    await state.finish()
