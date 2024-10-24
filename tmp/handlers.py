from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re
from aiogram import Bot

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT, ADMIN_CHAT_ID, TOKEN

from app.texts import *
from app.database import Database
from app.keyboards import *
# type: ignore
router = Router()
# db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
# bot = Bot(token=TOKEN)


""" # Блок хендлэров для админа 
@router.message(Command('query_q'))
async def query(message: Message, state: FSMContext):
    user_id = message.from_user.id
    query = '''SELECT role FROM users WHERE user_id = $1'''
    role = await db.fetch(query, user_id)
    if(role != 'admin'):
        pass
    else:
        await state.set_state(Admin.wait_query)
        await message.answer('select_q, delete_q, update_q, insert_q')
        
@router.message(Admin.wait_query and Command('select_q'))
async def query_select(message: Message, state: FSMContext):
    query = message.text
    response = await db.fetch(query=query)
    await state.clear()
    

@router.message(Admin.wait_query and (Command('delete_q') or Command('update_q') or Command('insert_q'))) 
async def query_delete(message: Message, state: FSMContext):
    query = message.text
    response = await db.execute(query=query)
    await state.clear()
"""
