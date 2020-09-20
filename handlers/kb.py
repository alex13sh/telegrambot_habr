from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

kb_start_1 = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row('/subscribe', '/unsubscribe', '/list_sub')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)\
        .row('Подписаться', 'Отписаться')\
        .add('Список подписок')
