import asyncio
import logging

from aiogram import Dispatcher

from app.handlers import setup_routers 
from app.handlers.conn import db, bot


dp = Dispatcher()

async def main():
    setup_routers(dp=dp)
    await on_startup(db=db)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(db=db)
    
async def on_startup(db):
    await db.connect()
    logging.info("Database connected.")

async def on_shutdown(db):
    await db.disconnect()
    logging.info("Database disconnected.")
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="bot_log.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disconnected')
        