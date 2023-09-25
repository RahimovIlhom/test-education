from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Kontaktni yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)