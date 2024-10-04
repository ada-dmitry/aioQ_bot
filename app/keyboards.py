from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


welcome_again_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Перейти в меню", callback_data='profile')],
   ])


review_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отчет с мероприятия", callback_data='rep_from_event')],
    [InlineKeyboardButton(text="Отзыв на куратора", callback_data='review_curator')]
   ])


# main_kb_list = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="👤 Профиль 👤", callback_data='profile')],
#         [InlineKeyboardButton(text="📈 Отчет о работе куратора 📉", callback_data='report')]
#     ])


# reg_kb_role = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Куратор', callback_data='curator')],
#     [InlineKeyboardButton(text='Первокурсник', callback_data='freshman')]
# ])

# start_reg_button = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="OK", callback_data='command:/reg')],  
#     ])

reg_role_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Куратор'), KeyboardButton(text='Первокурсник')]
],
                                  resize_keyboard=True
                                  )

start_reg_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поехали!')]
],
                                  resize_keyboard=True)

help_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👾 Тех.Поддержка 👾', callback_data='support')]
        # [InlineKeyboardButton(text='😎 Ст.Куратор 😎', callback_data='senior')]
    ])

standart_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сделать отметку в чек-листе')],
])

profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📈 Отчет о работе куратора 📉", callback_data='report')],
    [InlineKeyboardButton(text="🔴 Удалить аккаунт 🔴", callback_data='rereg')]
   ])



profile_kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить сообщение", callback_data='send_reply')]
   ])


profile_choise_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data='yes_prof')],
        [InlineKeyboardButton(text="Нет", callback_data='profile')]
    ])

report_freshman = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в начало", callback_data='start')]
    ])

def create_inline_keyboard(items):
    keyboard_builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки в клавиатуру
    for item in items:
        tmp = f'''item_{item}'''
        keyboard_builder.button(text=str(item), callback_data=tmp)
    keyboard_builder.button(text='Назад', callback_data='profile')
    # Генерация готовой клавиатуры
    return keyboard_builder.as_markup()

report_curator = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отчет", callback_data='rep_cur')],
        [InlineKeyboardButton(text="Чек-лист", callback_data='check_list')],
        [InlineKeyboardButton(text="Назад", callback_data='profile')]
    ])

def create_inline_keyboard(items):
    keyboard_builder = InlineKeyboardBuilder()
    
    for item in items:
        tmp = f'''group_{item}'''
        keyboard_builder.button(text=str(item), callback_data=tmp)
    keyboard_builder.button(text='Назад', callback_data='profile')
    return keyboard_builder.as_markup()
