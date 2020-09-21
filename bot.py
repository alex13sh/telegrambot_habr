#from datetime import datetime

from aiogram import executor
from misc import dp
import handlers
import db
db.init_base()
from parser import stopgame

dp.loop.create_task(stopgame.scheduled(2))
# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
