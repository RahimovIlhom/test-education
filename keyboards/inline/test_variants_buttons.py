import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def variants_buttons(test: list):
    btn1 = InlineKeyboardButton(text=test[2], callback_data='true')
    btn2 = InlineKeyboardButton(text=test[3], callback_data='false')
    btn3 = InlineKeyboardButton(text=test[4], callback_data='false')
    btn4 = InlineKeyboardButton(text=test[5], callback_data='false')
    inlines = random.sample([btn1, btn2, btn3, btn4], 4)
    variants = InlineKeyboardMarkup(row_width=2)
    variants.add(inlines[0], inlines[1])
    variants.add(inlines[2], inlines[3])
    return variants
