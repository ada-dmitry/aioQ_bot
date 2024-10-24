from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from app.texts import *
from app.keyboards import *
from app.handlers.conn import bot

admin_router = Router()

class Admin(StatesGroup):
    send_user_id = State()
    send_message = State()
    wait_query = State()

@admin_router.callback_query(lambda c: c.data in ['send_reply'])
async def reply_from_admin_1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.send_user_id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''Введите user_id пользователя,\
которому вы хотите отправить сообщение (его можно взять из беседы ТП)''',
                                reply_markup=None)
    
@admin_router.message(Admin.send_user_id)
async def reply_from_admin_2(message: Message, state: FSMContext):
    await state.update_data(send_user_id=message.text)
    await state.set_state(Admin.send_message)
    await message.reply(f'Отправьте сообщение для этого пользователя')
    
@admin_router.message(Admin.send_message)
async def reply_from_admin_3(message: Message, state: FSMContext):
    tmp = await state.get_data()
    user_id = tmp['send_user_id']
    await state.set_state(Admin.send_message)
    await state.clear()
    await bot.send_message(chat_id=user_id, text=message.text)
    await message.answer('Сообщение отправлено.', reply_markup=profile_kb_admin)
    