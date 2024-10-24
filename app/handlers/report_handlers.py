from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import ADMIN_CHAT_ID

from app.texts import *
from app.keyboards import *
from app.handlers.conn import bot, db

report_router = Router()

class Report_Fresh(StatesGroup):
    choice_review = State()
    send_photo = State()
    send_name = State()
    send_review = State()
    
class Report_Cur(StatesGroup):
    send_name = State()
    send_photo = State()
    choice_group = State()


async def curators_from_group_num(group_number: str) -> list:
    """Функция для вывода кураторов по заданной группе
    Args:
        group_number (str): группа пользователя (выбирается запросом из БД)
    Returns:
        curators (list): Список кураторов группы
    """    
    query = f'''SELECT full_name FROM users WHERE (c_group_1 = $1) OR (c_group_2 = $2)'''
    curators = []
    tmp1 = await db.fetch(query, group_number, group_number) 
    for i in tmp1:
        curators.append(i['full_name'])
    return curators
         
@report_router.callback_query(lambda c: c.data in ['report'])
async def report_choice(callback_query: CallbackQuery):
    """Функция отчета для кураторов и первокурсников

    Args:
        callback_query (CallbackQuery): Ответ от клавиатуры (отчет, чек-лист, удалить аккаунт)
    """    
    user_id = callback_query.from_user.id
    query = f"""SELECT role, group_number FROM users WHERE user_id = $1"""
    tmp1 = await db.fetch(query, user_id)
    tmp2 = tmp1[0]
    role = tmp2['role'] 
    group_num = str(tmp2['group_number'])
    if(role == 'freshman'): 
        curators_data = await curators_from_group_num(group_number=group_num)
        cur_names = []
        for i in range(len(curators_data)):
            cur_names.append(curators_data[i])
        keyboard = create_inline_keyboard(curators_data)
        
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=f'''Ваша группа: {group_num}\nВаши кураторы: {", ".join(str(x) for x in cur_names)}
Вы можете выбрать куратора, о работе которого хотите отчитаться, ниже.''',
                                    reply_markup=keyboard) 
    elif(role == 'curator'):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=f'''Вы - куратор.\nУ вас есть определенные обязанности, \
основные из которых перечислены в чек-листе, доступном по кнопке ниже.\nДля отчета - нажмите на кнопку "Отчет" и отправьте фото-подтверждение, \
после обработки модераторами вам придет подтверждение.''',
                                    reply_markup=report_curator) 
        
@report_router.callback_query(lambda c: c.data in ['check_list'])
async def get_check_list(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data='report')]
    ])
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=checklist_curator,
                                    reply_markup=keyboard) 
    
@report_router.callback_query(lambda c: c.data in ['rep_cur'])
async def take_report_curtor_1(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await state.set_state(Report_Cur.choice_group)
    query = """SELECT c_group_1, c_group_2 FROM users WHERE user_id = $1"""
    tmp = await db.fetch(query, user_id)
    tmp1 = tmp[0]
    grps = [tmp1['c_group_1'], tmp1['c_group_2']]
    # print('я люблю тебя')
    if(grps[1] == None):
        keyboard = create_inline_keyboard(grps[0:1])
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=f'О какой группе вы хотите отчитаться?',
                                    reply_markup=keyboard)
    else:
        keyboard = create_inline_keyboard(grps)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=f'О какой группе вы хотите отчитаться?',
                                    reply_markup=keyboard)
    
@report_router.callback_query(lambda c: c.data and c.data.startswith('group_') and Report_Cur.choice_group)
async def take_report_curator_2(callback_query: CallbackQuery, state: FSMContext):
    selected_option = callback_query.data.replace('group_', '')
    await state.update_data(group=selected_option)
    await state.set_state(Report_Cur.send_name)
    
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=f'Введите название мероприятия/события.',
                                    reply_markup=None)
    
@report_router.message(Report_Cur.send_name)
async def take_report_curator_3(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Report_Cur.send_photo)
    await message.answer('Отправьте фото подтверждение (на фото должны быть вы и какие-то ориентиры мероприятия)')
    
@report_router.message(Report_Cur.send_photo and F.photo)
async def take_report_curator_4(message: Message, state: FSMContext):
    current_data = await state.get_data()
    await state.clear()
    photo = message.photo[-1]
    user_id = message.from_user.id 
    username = message.from_user.username
    event = current_data['name']
    group = current_data['group']
    await bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo.file_id, caption=f"Фото переслано от @{username} (id: {user_id})\n\
Название мероприятия: {event}\nГруппа: {group}")
    await message.answer('Сообщение отправлено на проверку модераторам.\nПосле проверки вам придет подтверждение.\n\
Спасибо за сотрудничество!', reply_markup=profile_kb)

    
@report_router.callback_query(lambda c: c.data and c.data.startswith('item_'))
async def handle_callback(callback_query: CallbackQuery, state: FSMContext):
    selected_option = callback_query.data.replace('item_', '')
    await bot.answer_callback_query(callback_query.id)

    await state.set_state(Report_Fresh.choice_review)
    await state.update_data(name=selected_option)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text='Если вы хотите отблагодарить куратора за то,\
что он порекомендовал вам что-то, что вам понравилось, то вы можете отправить фото c мероприятия.\n\
Так же вы можете просто оставить отзыв о кураторе, если хотите\
(отзыв анонимный, личность не раскроет никто, содержание смогут увидеть старшие кураторы).',
                                    reply_markup=review_kb) 


@report_router.callback_query(lambda c: c.data in ['rep_from_event'] and Report_Fresh.choice_review)  
async def take_photo(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Report_Fresh.send_photo)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text='Отправьте фотографию, по которой можно подтвердить, что вы находитесь на мероприятии.',
                                    reply_markup=None) 

@report_router.message(Report_Fresh.send_photo and F.photo)
async def take_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    username = message.from_user.username
    await state.update_data(photo=photo.file_id)
    await state.set_state(Report_Fresh.send_name)
    await message.answer("Напишите, пожалуйста, название мероприятия.")
    
@report_router.message(Report_Fresh.send_name)
async def take_name_event(message: Message, state: FSMContext):
    await state.update_data(name_of_event=message.text)

    await state.set_state(Report_Fresh.send_review)
    await message.answer(f'''Напишите небольшой отзыв о работе куратора, если необходимо.\nВ обратном случае отправьте прочерк.''')
    
    
@report_router.callback_query(lambda c: c.data in ['review_curator'] and Report_Fresh.choice_review)
async def pre_take_review(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Report_Fresh.send_review)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text='Напишите небольшой отзыв о работе куратора.',
                                    reply_markup=None) 
    
@report_router.message(Report_Fresh.send_review)
async def take_review(message: Message, state: FSMContext):
    tmp = await state.get_data()
    username = message.from_user.username
    name = tmp['name']
    photo = tmp.get('photo')
    await state.clear()
    if(photo != None):
        event = tmp['name_of_event']
        await bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo, caption=f"Фото переслано от @{username}\n\
Название мероприятия: {event}\nОтзыв на куратора {name}: {message.text}")
    else:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'Отзыв на куратора {name}: {message.text}')
    