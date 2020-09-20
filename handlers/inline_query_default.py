from aiogram import types
from misc import dp, bot, LIST_SEARCH_TAGS

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
import hashlib

LIST_TAGS = LIST_SEARCH_TAGS

@dp.inline_handler(lambda q: q.query.startswith("#"))
async def inline_handler(inline_query: InlineQuery):
    _startwith = inline_query.query[1:].lower()
    items = []
    for i, tag in enumerate(LIST_TAGS):
        if not tag.lower().startswith(_startwith): continue
        inline_kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                'Использовать тег', 
                switch_inline_query_current_chat=f'#{tag}'
            ))
        item = InlineQueryResultArticle(
            id=i,
            title=f'Tag: {tag}',
            input_message_content=InputTextMessageContent(f'Tag: {tag}'),
            reply_markup=inline_kb
        )
        items.append(item)
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=100)

@dp.inline_handler()
async def inline_handler(inline_query: InlineQuery):
    await bot.answer_inline_query(inline_query.id, results=[], cache_time=1)
