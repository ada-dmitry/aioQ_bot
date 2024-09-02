from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT

from app.texts import help, welcome
from app.database import Database
from app.keyboards import main_kb_list

router = Router()
db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(welcome, reply_markup=main_kb_list)
    
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(help)
    
# @router.message(F.text == 'Test')
# async def test_db(message: Message):
#     user_id = message.from_user.id
#     text = message.text
#     query = 'INSERT INTO users(user_id, full_name) VALUES ($1, $2)'
    
#     await db.execute(query, user_id, text)
#     await message.reply("Message saved!")

@router.message(Command('reg'))
async def start_register(message: Message):
    user_id = message.from_user.id
    await message.answer('Meow')
    
@router.callback_query(lambda c: c.data and c.data.startswith('command:'))
async def process_callback_command(callback_query: CallbackQuery):
    command = callback_query.data.split(':')[1]
    # Имитация отправки команды
    if command == '/reg':
        await start_register(callback_query.message)
    

# @router.message(Command('reg'))
# async def re_register(message: Message):
#     await 
