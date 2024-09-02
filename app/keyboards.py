from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)


main_kb_list = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Зарегистрироваться", callback_data='command:/reg')],
        [InlineKeyboardButton(text="👤 Профиль", callback_data='command:/profile')]
    ])