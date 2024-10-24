from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import ADMIN_CHAT_ID

from app.texts import *
from app.keyboards import *
from app.handlers.conn import bot

support_router = Router()

class Help(StatesGroup):
    wait_support = State()

@support_router.message(Command('help'))
@support_router.message(F.text == 'Помощь')
async def get_help(message: Message):
    await message.answer(help, reply_markup=help_kb)
    
@support_router.callback_query(lambda c: c.data in ['support']) 
async def get_support(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Help.wait_support)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text='Опишите проблему/жалобу/предложение ОДНИМ сообщением: ',
                                reply_markup=None)
    
@support_router.message(Help.wait_support)
async def forward_support(message: Message, state: FSMContext):
    await bot.send_message(ADMIN_CHAT_ID, f"Новое сообщение в техподдержку от пользователя @{message.from_user.username} (ID: {message.from_user.id}):")
    await message.forward(ADMIN_CHAT_ID)
    await message.reply("Ваше сообщение отправлено в техподдержку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()