from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

successful = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tayyorman", callback_data='successful_test')],
    ],
    row_width=1
)
