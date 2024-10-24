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
        