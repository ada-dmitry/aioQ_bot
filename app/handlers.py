from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re
from aiogram import Bot

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT, ADMIN_CHAT_ID, TOKEN, SENIOR_CHAT_ID

from app.texts import *
from app.database import Database
from app.keyboards import *

router = Router()
db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
bot = Bot(token=TOKEN)

class Register(StatesGroup):
    name = State()
    role = State()
    group_number = State()
    curator_groups = State()
    
class Help(StatesGroup):
    wait_support = State()
    wait_senior = State()
    
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
@router.message(F.text == 'Помощь')
async def get_help(message: Message):
    await message.answer(help, reply_markup=help_kb)
    
@router.message(F.text == '👾 Тех.Поддержка 👾')
async def get_support(message: Message, state: FSMContext):
    await state.set_state(Help.wait_support)
    await message.answer('Опишите проблему/жалобу/предложение ОДНИМ сообщением: ')
    
@router.message(F.text == '😎 Ст.Куратор 😎')
async def get_support(message: Message, state: FSMContext):
        await state.set_state(Help.wait_senior)
        await message.answer('Напишите обращение к старшему куратору ОДНИМ сообщением: ')  

@router.message(Help.wait_support)
async def forward_support(message: Message, state: FSMContext):
    await bot.send_message(ADMIN_CHAT_ID, f"Новое сообщение в техподдержку от пользователя @{message.from_user.username} (ID: {message.from_user.id}):")
    await message.forward(ADMIN_CHAT_ID)
    await message.reply("Ваше сообщение отправлено в техподдержку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()
    
@router.message(Help.wait_senior)
async def forward_support(message: Message, state: FSMContext):
    await bot.send_message(SENIOR_CHAT_ID, f"Новое сообщение для ст.кураторов от пользователя @{message.from_user.username} (ID: {message.from_user.id}):")
    await message.forward(SENIOR_CHAT_ID)
    await message.reply("Ваше сообщение отправлено старшим кураторам. Мы свяжемся с вами в ближайшее время.")
    await state.clear()

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
    if(role == 'Первокурсник'):
        await state.update_data(role='freshman')
    else:
        await state.update_data(role='curator')
    
    await state.set_state(Register.group_number)
    await message.answer('Введите свою группу (в которой вы учитесь): ', reply_markup=ReplyKeyboardRemove())
    
@router.message(Register.group_number)
async def process_group(message: Message, state: FSMContext):
    user_id = message.from_user.id
    pattern = r'^[БСМА]\d{2}-\d{3}$'
    group_number = message.text
    if not re.match(pattern, group_number):
        await message.reply("Некорректный формат группы. Пожалуйста, введите группу в формате: БXX-XXX (СXX-XXX)")
    else:
        await state.update_data(group_number=group_number)
        current_data = await state.get_data()
        role = current_data['role']
        if(role == 'freshman'):
            query = """INSERT INTO users(user_id, full_name, role, group_number) VALUES ($1, $2, $3, $4)"""
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group_number'])
            await state.clear()
            await message.answer("Регистрация завершена!")
        elif(role == 'curator'):
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
            query = 'INSERT INTO users (user_id, full_name, role, group_number, c_group_1) VALUES ($1, $2, $3, $4, $5)'
            print(current_data)
            await state.clear()
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group_number'], groups[0])
            await message.answer("Регистрация завершена!")
        elif(ln==2):
            query = 'INSERT INTO users(user_id, full_name, role, group_number, c_group_1, c_group_2) VALUES ($1, $2, $3, $4, $5, $6)'
            await state.clear()
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group_number'], groups[0], groups[1])
            await message.answer("Регистрация завершена!")
        