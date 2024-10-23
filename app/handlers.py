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

class Report_Fresh(StatesGroup):
    choice_review = State()
    send_photo = State()
    send_name = State()
    send_review = State()
    
class Report_Cur(StatesGroup):
    send_name = State()
    send_photo = State()
    choice_group = State()

class Admin(StatesGroup):
    send_user_id = State()
    send_message = State()
    wait_query = State()
    
async def curators_from_group_num(group_number: str) -> list:
    """Функция для вывода кураторов по заданной группе

    Args:
        group_number (str): группа пользователя (выбирается запросом из БД)

    Returns:
        list: Список кураторов группы
    """    
    query = f'''SELECT full_name FROM users WHERE (c_group_1 = $1) OR (c_group_2 = $2)'''
    curators = []
    tmp1 = await db.fetch(query, group_number, group_number)
    for i in tmp1:
        curators.append(i['full_name'])
    return curators
         
    
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Функция старта бота /start

    Args:
        message (Message): сообщение пользователя
    """    
    user_id = message.from_user.id
    query = 'SELECT * FROM users WHERE user_id = $1'
    db_response = await db.fetch(query, user_id)
    if(db_response == []):
        await message.answer(welcome, reply_markup=start_reg_button)
    else:
        await message.answer(welcome_again, reply_markup=welcome_again_kb)
        
@router.callback_query(lambda c: c.data in ['report'])
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
        
@router.callback_query(lambda c: c.data in ['check_list'])
async def get_check_list(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data='report')]
    ])
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=checklist_curator,
                                    reply_markup=keyboard) 
    
@router.callback_query(lambda c: c.data in ['rep_cur'])
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
    
@router.callback_query(lambda c: c.data and c.data.startswith('group_') and Report_Cur.choice_group)
async def take_report_curator_2(callback_query: CallbackQuery, state: FSMContext):
    selected_option = callback_query.data.replace('group_', '')
    await state.update_data(group=selected_option)
    await state.set_state(Report_Cur.send_name)
    
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text=f'Введите название мероприятия/события.',
                                    reply_markup=None)
    
@router.message(Report_Cur.send_name)
async def take_report_curator_3(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Report_Cur.send_photo)
    await message.answer('Отправьте фото подтверждение (на фото должны быть вы и какие-то ориентиры мероприятия)')
    
@router.message(Report_Cur.send_photo and F.photo)
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

    
@router.callback_query(lambda c: c.data and c.data.startswith('item_'))
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


@router.callback_query(lambda c: c.data in ['rep_from_event'] and Report_Fresh.choice_review)  
async def take_photo(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Report_Fresh.send_photo)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text='Отправьте фотографию, по которой можно подтвердить, что вы находитесь на мероприятии.',
                                    reply_markup=None) 

@router.message(Report_Fresh.send_photo and F.photo)
async def take_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    username = message.from_user.username
    await state.update_data(photo=photo.file_id)
    await state.set_state(Report_Fresh.send_name)
    await message.answer("Напишите, пожалуйста, название мероприятия.")
    
@router.message(Report_Fresh.send_name)
async def take_name_event(message: Message, state: FSMContext):
    await state.update_data(name_of_event=message.text)

    await state.set_state(Report_Fresh.send_review)
    await message.answer(f'''Напишите небольшой отзыв о работе куратора, если необходимо.\nВ обратном случае отправьте прочерк.''')
    
    
@router.callback_query(lambda c: c.data in ['review_curator'] and Report_Fresh.choice_review)
async def pre_take_review(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Report_Fresh.send_review)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text='Напишите небольшой отзыв о работе куратора.',
                                    reply_markup=None) 
    
@router.message(Report_Fresh.send_review)
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
    
        
''' Блок команд для профиля '''

@router.callback_query(lambda c: c.data in ['profile'])        
@router.callback_query(Command('profile'))
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
                                text=f'''***Ваш профиль:***\nФИО: _{full_name}_\nРоль: _{role}_\nГруппа: _{group_number}_''',
                                reply_markup=profile_kb)
        await bot.answer_callback_query(callback_query.id)
    elif(role == 'Куратор'):
        group_1 = usr['c_group_1']
        group_2 = usr['c_group_2']
        if(group_2!=None):
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''***Ваш профиль:***\nФИО: {full_name}\nРоль: {role}\nГруппа: {group_number}\n\
# Группы на кураторстве:\n{group_1.strip()}, {group_2.strip()}''',
                                reply_markup=profile_kb)
            await bot.answer_callback_query(callback_query.id)
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''***Ваш профиль:***\nФИО: {full_name}\nРоль: {role}\nГруппа: {group_number}\n\
# Группы на кураторстве: {group_1}''',
                                reply_markup=profile_kb)
            await bot.answer_callback_query(callback_query.id)
    elif(role == 'Модератор'):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''**Ваш профиль:**\nФИО: _{full_name}_\nРоль: _{role}_''',
                                reply_markup=profile_kb_admin)
        await bot.answer_callback_query(callback_query.id)
        
''' Блок команд для отправки отчета '''
        
@router.callback_query(lambda c: c.data in ['send_reply'])
async def reply_from_admin_1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.send_user_id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text=f'''Введите user_id пользователя,\
которому вы хотите отправить сообщение (его можно взять из беседы ТП)''',
                                reply_markup=None)
    
@router.message(Admin.send_user_id)
async def reply_from_admin_2(message: Message, state: FSMContext):
    await state.update_data(send_user_id=message.text)
    await state.set_state(Admin.send_message)
    await message.reply(f'Отправьте сообщение для этого пользователя')
    
@router.message(Admin.send_message)
async def reply_from_admin_3(message: Message, state: FSMContext):
    tmp = await state.get_data()
    user_id = tmp['send_user_id']
    await state.set_state(Admin.send_message)
    await state.clear()
    await bot.send_message(chat_id=user_id, text=message.text)
    await message.answer('Сообщение отправлено.', reply_markup=profile_kb_admin)
    
    
''' Блок команд для вызова справки и ТП '''    
    
@router.message(Command('help'))
@router.message(F.text == 'Помощь')
async def get_help(message: Message):
    await message.answer(help, reply_markup=help_kb)
    
@router.callback_query(lambda c: c.data in ['support']) 
async def get_support(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Help.wait_support)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id, 
                                text='Опишите проблему/жалобу/предложение ОДНИМ сообщением: ',
                                reply_markup=None)
    
@router.message(Help.wait_support)
async def forward_support(message: Message, state: FSMContext):
    await bot.send_message(ADMIN_CHAT_ID, f"Новое сообщение в техподдержку от пользователя @{message.from_user.username} (ID: {message.from_user.id}):")
    await message.forward(ADMIN_CHAT_ID)
    await message.reply("Ваше сообщение отправлено в техподдержку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()

''' Блок хендлэров для регистрации '''

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
