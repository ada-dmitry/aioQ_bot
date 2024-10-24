from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re
from aiogram import Bot

class Register(StatesGroup):
    name = State()
    role = State()
    group_number = State()
    curator_groups = State()
    
@router.message(Command('reg'))
@router.message(F.text == 'Поехали!')
async def start_register(message: Message | CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    query = """DELETE FROM users WHERE user_id = $1"""
    await db.execute(query, user_id)
    await message.answer('Введите ваше ФИО: ')
    await state.set_state(Register.name)
    
@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    if(len(name) > 100): await message.answer('Слишком длинное ФИО. Укажите имя менее 100 символов суммарно.')
    else:
        await state.update_data(name=message.text)
        await state.set_state(Register.role)
        await message.answer('Выберите вашу роль: ', reply_markup=reg_role_kb)
    
@router.message(Register.role)
async def process_role(message: Message, state: FSMContext):
    role = message.text
    if(role == 'Первокурсник'):
        await state.update_data(role='freshman')
        await state.set_state(Register.group_number)
        await message.answer('Введите свою группу (в которой вы учитесь): ', reply_markup=ReplyKeyboardRemove())
    elif(role == 'Куратор'):
        await state.update_data(role='curator')
        await state.set_state(Register.group_number)
        await message.answer('Введите свою группу (в которой вы учитесь): ', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Выберите роль из предложенных вариантов: ')
    
    
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
            await message.answer("Регистрация завершена!", reply_markup=profile_kb)
        elif(role == 'curator'):
            await state.set_state(Register.curator_groups)
            await message.answer('Введите вашу(-ы) группу(-ы) через пробел: ')

@router.message(Register.curator_groups)
async def process_cur_groups(message: Message, state: FSMContext):
    user_id = message.from_user.id
    pattern = r'^[БСМА]\d{2}-\d{3}$'
    groups = [i.strip() for i in message.text.split()]
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
            await state.clear()
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group_number'], groups[0])
            await message.answer("Регистрация завершена!", reply_markup=profile_kb)
        elif(ln==2):
            query = 'INSERT INTO users(user_id, full_name, role, group_number, c_group_1, c_group_2) VALUES ($1, $2, $3, $4, $5, $6)'
            await state.clear()
            await db.execute(query, user_id, current_data['name'], current_data['role'], current_data['group_number'], groups[0], groups[1])
            await message.answer("Регистрация завершена!", reply_markup=profile_kb)
        
@router.callback_query(lambda c: c.data in ['rereg']) 
async def del_user_1(callback_query: CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text='Вы уверены, что хотите удалить аккаунт и заново пройти регистрацию?',
                                reply_markup=profile_choise_kb) 
    await bot.answer_callback_query(callback_query.id)

    
@router.callback_query(lambda c: c.data in ['yes_prof']) 
async def del_user_2(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    query = """DELETE FROM users WHERE user_id = $1"""
    await db.execute(query, user_id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text='Ваш профиль удален. Введите /start для повторной регистрации.',
                                reply_markup=None) 
    await bot.answer_callback_query(callback_query.id)