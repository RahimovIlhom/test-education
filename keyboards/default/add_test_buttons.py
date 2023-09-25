from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

add_test_bot = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📥 Test qo'shish"),
         KeyboardButton(text="🗒 Testlarni ko'rish"),
         ]
    ],
    resize_keyboard=True
)

skip_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏭ O'tkazib yuborish")]
    ],
    resize_keyboard=True
)
