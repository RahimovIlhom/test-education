import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import ContentType
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default import skip_button
from loader import dp, db, bot
from states import TestStateGroup


@dp.message_handler(Command('send_post'), user_id=ADMINS)
async def send_post(msg: types.Message):
    try:
        post = msg.reply_to_message.text
        user_ids = db.select_users_ids()
        for user_id in user_ids:
            await bot.send_message(chat_id=user_id, text=post)
            await asyncio.sleep(0.05)
    except AttributeError as err:
        await msg.reply("Post yuborib keyin unga javob tariqasida /send_post buyruqni yuboring!")
        print(err)


@dp.message_handler(Command('all_users'), user_id=ADMINS)
async def allUsers(msg: types.Message):
    users = db.select_users()
    await msg.answer(f"{users}")


@dp.message_handler(Command('del_users'), user_id=ADMINS)
async def del_users(msg: types.Message):
    db.delete_users()
    await msg.answer("Baza tozalandi!")
