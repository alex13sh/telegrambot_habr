from aiogram import types
from misc import dp

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)
    
#@dp.message_handler()
#async def echo_message(msg: types.Message):
    #await bot.send_message(msg.from_user.id, msg.text) 
