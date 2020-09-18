#import asyncio
#from datetime import datetime

from aiogram import executor
from misc import dp
import handlers


# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
