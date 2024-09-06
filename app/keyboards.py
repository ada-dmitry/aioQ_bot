from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)


main_kb_list = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль 👤", callback_data='command:/profile')],
        
    ])

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
                                  resize_keyboard=True)

start_reg_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поехали!')]
],
                                  resize_keyboard=True)
