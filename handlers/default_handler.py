from aiogram import types
from misc import dp, bot

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)
    
#@dp.message_handler()
#async def echo_message(msg: types.Message):
    #await bot.send_message(msg.from_user.id, msg.text) 

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
import hashlib

@dp.inline_handler()
async def inline_handler(inline_query: InlineQuery):
    await bot.answer_inline_query(inline_query.id, results=[], cache_time=1)
