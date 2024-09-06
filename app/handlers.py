from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT

from app.texts import *
from app.database import Database
from app.keyboards import *

router = Router()
db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

class Register(StatesGroup):
    name = State()
    role = State()
    group = State()
    curator_groups = State()
    
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    query = 'SELECT * FROM users WHERE user_id = $1'  
    db_response = await db.fetch(query, user_id)
    if(db_response == []):
        await message.answer(welcome, reply_markup=start_reg_button)
    else:
        await message.answer(welcome_again, reply_markup=main_kb_list)
    
    
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
@router.message(F.text == 'Поехали!')
async def start_register(message: Message | CallbackQuery, state: FSMContext):
    await message.answer('Введите ваше ФИО: ')
    await state.set_state(Register.name)
    
@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.role)
    await message.answer('Выберите вашу роль: ', reply_markup=reg_role_kb)
    
@router.message(Register.role)
async def process_role(message: Message, state: FSMContext):
    role = message.text
    await state.update_data(role=role)
    await state.set_state(Register.group)
    await message.answer('Введите свою группу (в которой вы учитесь): ')
    
@router.message(Register.group)
async def process_group(message: Message, state: FSMContext):
    user_id = message.from_user.id
    pattern = r'^[БСМА]\d{2}-\d{3}$'
    group = message.text
    if not re.match(pattern, group):
        await message.reply("Некорректный формат группы. Пожалуйста, введите группу в формате: БXX-XXX (СXX-XXX)")
    else:
        await state.update_data(group=group)
        current_data = await state.get_data()
        role = current_data['role']
        if(role == 'Первокурсник'):
            await state.clear()
            query = 'INSERT INTO users(user_id, full_name, role, group) VALUES ($1, $2, $3, $4)'
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group'])
            await message.answer("Регистрация завершена!")
        elif(role == 'Куратор'):
            await state.set_state(Register.curator_groups)
            await message.answer('Введите вашу(-ы) группу(-ы) через пробел: ')

@router.message(Register.curator_groups)
async def process_cur_groups(message: Message, state: FSMContext):
    user_id = message.from_user.id
    pattern = r'^[БСМА]\d{2}-\d{3}$'
    groups = message.text.split()
    current_data = await state.get_data()
    ln = len(groups)
    flag = 0
    for i in range(ln):
        if not re.match(pattern, groups[i]):
            flag += 1
    if(flag!=0): await message.reply("Некорректный формат группы.\
 Пожалуйста, введите группы в формате: БXX-XXX (СXX-XXX)")
    else:
        if(ln==1):
            query = 'INSERT INTO users(user_id, full_name, role, group, c_group_1) VALUES ($1, $2, $3, $4, $5)'
            await state.clear()
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group'], groups[0])
            await message.answer("Регистрация завершена!")
        elif(ln==2):
            query = 'INSERT INTO users(user_id, full_name, role, group, c_group_1, c_group_2) VALUES ($1, $2, $3, $4, $5, $6)'
            await state.clear()
            await db.execute(query, user_id, current_data['name'],\
                current_data['role'], current_data['group'], groups[0], groups[1])
            await message.answer("Регистрация завершена!")
        
    

    
    
            
            

            
        

    

# async def start_register(message: Message):
#     user_id = message.from_user.id 
#     await message.
    
    
#     await message.reply(f"Done")
    
    
# @router.message(Command('reg'))
# async def re_register(message: Message):
#     await 
