from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram import Router

from app.texts import *
from app.keyboards import *
from app.handlers.conn import bot, db


profile_router = Router()



@profile_router.callback_query(lambda c: c.data in ['profile'])        
@profile_router.callback_query(Command('profile'))
async def get_profile(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    query = """SELECT full_name, role, group_number, c_group_1, c_group_2 FROM users WHERE user_id = $1"""
    data = await db.fetch(query, user_id)
    usr = data[0]
    full_name = usr['full_name']
    if(usr['role'] == 'curator'): role = 'Куратор'
    elif(usr['role'] == 'freshman'): role = 'Первокурсник'
    elif(usr['role'] == 'admin'): role = 'Модератор'
    group_number = usr['group_number']
    if(role == 'Первокурсник'):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''Ваш профиль:\nФИО: {full_name}\nРоль: {role}\nГруппа: {group_number}''',
                                reply_markup=profile_kb)
        await bot.answer_callback_query(callback_query.id)
    elif(role == 'Куратор'):
        group_1 = usr['c_group_1']
        group_2 = usr['c_group_2']
        if(group_2!=None):
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''Ваш профиль:\nФИО: {full_name}\nРоль: {role}\nГруппа: {group_number}\n\
Группы на кураторстве:\n{group_1.strip()}, {group_2.strip()}''',
                                reply_markup=profile_kb)
            await bot.answer_callback_query(callback_query.id)
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''Ваш профиль:\nФИО: {full_name}\nРоль: {role}\nГруппа: {group_number}\n\
Группы на кураторстве: {group_1}''',
                                reply_markup=profile_kb)
            await bot.answer_callback_query(callback_query.id)
    elif(role == 'Модератор'):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''Ваш профиль:\nФИО: {full_name}\nРоль: {role}''',
                                reply_markup=profile_kb_admin)
        await bot.answer_callback_query(callback_query.id)