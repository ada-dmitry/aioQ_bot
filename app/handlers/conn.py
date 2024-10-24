from aiogram import Bot

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT, TOKEN

from app.texts import *
from app.database import Database
from app.keyboards import *

db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
bot = Bot(token=TOKEN)