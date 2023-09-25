from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, db


@dp.message_handler(Command('info'))
async def send_info(msg: types.Message):
    user_id = msg.from_user.id
    user = db.select_user(user_id)
    info = "Ma'lumotlaringiz!\n"
    info += f"Ism-familiyangiz: {user[1]}\n" \
            f"Telefon nomeringiz: {user[2]}\n" \
            f"Emailingiz: {user[3]}\n" \
            f"Tug'ilgan kuningiz: {user[4]}"
    await msg.answer(info)


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)

