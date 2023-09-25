from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(Command('set_email'))
async def email_command(msg: types.Message, state: FSMContext):
    await msg.answer("Emailingizni yuboring: ")
    await state.set_state('user_email')


@dp.message_handler(state='user_email')
async def email_send(msg: types.Message, state: FSMContext):
    email = msg.text
    user_id = msg.from_user.id
    db.update_email(user_id, email)
    await msg.answer("Emailingiz muvaffaqiyatli o'zgartirildi!")
    await state.finish()


@dp.message_handler(Command('set_number'))
async def phone_command(msg: types.Message, state: FSMContext):
    await msg.answer("Telefon raqamingizni yuboring: ")
    await state.set_state('user_number')


@dp.message_handler(state='user_number')
async def phone_send(msg: types.Message, state: FSMContext):
    phone_number = msg.text
    user_id = msg.from_user.id
    db.update_number(user_id, phone_number)
    await msg.answer("Telefon raqamingiz muvaffaqiyatli o'zgartirildi!")
    await state.finish()


@dp.message_handler(Command('set_birthday'))
async def birthday_command(msg: types.Message, state: FSMContext):
    await msg.answer("Tug'ilgan kuningizni yuboring\n"
                     "Yubrorish tartibi (12-12-2002 yoki 12.12.2002): ")
    await state.set_state('user_birthday')


@dp.message_handler(state='user_birthday')
async def birthday_send(msg: types.Message, state: FSMContext):
    birthday = msg.text
    user_id = msg.from_user.id
    db.update_birthday(user_id, birthday)
    await msg.answer("Tug'ilgan kuningiz muvaffaqiyatli o'zgartirildi!")
    await state.finish()


@dp.message_handler(Command('set_fullname'))
async def name_command(msg: types.Message, state: FSMContext):
    await msg.answer("Ism-familiyangizni yuboring: ")
    await state.set_state('user_name')


@dp.message_handler(state='user_name')
async def name_send(msg: types.Message, state: FSMContext):
    name = msg.text
    user_id = msg.from_user.id
    db.update_fullname(user_id, name)
    await msg.answer("Ism-familiyangiz muvaffaqiyatli o'zgartirildi!")
    await state.finish()


@dp.message_handler(Command('del_tests'), user_id=ADMINS)
async def delete_all_tests(msg: types.Message):
    db.delete_tests()
    await msg.answer("Barcha testlar o'chirildi!")

