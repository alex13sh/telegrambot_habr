from aiogram import types
from misc import dp

# Команда активации подписки
@dp.message_handler(commands=['start'])
async def start(message: types.Message):    
    if len(message.text) > len("/start "): 
        message.text = message.text[7:]
        #await message.answer("Реферальный текст: "+message.text)
        if message.text[0] == "_":
            if message.text.startswith("_subscribe"):
                message.text = "/" + message.text[1:10] + " " + message.text[11:]
                await subscribe(message)
    else:
        await message.answer("Добро пожаловать в тестовый бот для Habr и StopGame")

# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    name = None
    if len(message.text) > 10:
        name = message.text[11:]
    if name: 
        await message.answer("Вы успешно подписались на рассылку! По имени: "+name)
    else:
        await message.answer("На кого хотите подписаться? Укажите имя:")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    await message.answer("Вы успешно отписаны от рассылки.")
    await message.reply("Ну и ладно!")

