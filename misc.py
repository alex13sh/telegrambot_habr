import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

bot = Bot(token="1282150943:AAG758zak155FnoFYJSHuLhDA-EUaNHBPSg")
memory_storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=memory_storage, loop=loop)
logging.basicConfig(level=logging.INFO)

LIST_SEARCH_TAGS = []
