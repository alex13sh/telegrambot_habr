from aiogram import types
from misc import dp

from . import subs
from . import start

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    await message.answer("Вы успешно отписаны от рассылки.")
    await message.reply("Ну и ладно!")


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    if message.from_user.id == 1234567:  # Подставьте сюда свой Telegram ID
        commands = [types.BotCommand(command="/drinks", description="Заказать напитки"),
                    types.BotCommand(command="/food", description="Заказать блюда")]
        await bot.set_my_commands(commands)
        await message.answer("Команды настроены.")
