from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Saqlash", callback_data='true'),
         InlineKeyboardButton(text="Tahrirlash", callback_data='false')
         ],
    ],
    row_width=1
)
