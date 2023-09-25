from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

full_signup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="To'liq ro'yxatdan o'tish", callback_data='full_signup')],
    ],
    row_width=1
)
