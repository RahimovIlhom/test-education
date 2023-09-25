from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from data.config import ADMINS
from keyboards.default import phone, test, add_test_bot
from loader import dp, db, bot


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start_admin(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in db.select_users_ids():
        await message.answer("Bot qayta ishga tushdi", reply_markup=add_test_bot)
        return
    await message.answer(f"Salom, {message.from_user.full_name}!\n"
                         f"Botdan foydalanish uchun kontaktingizni yuboring.", reply_markup=phone)
    await state.set_state('phone')


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in db.select_users_ids():
        await message.answer("Bot qayta ishga tushdi", reply_markup=test)
        return
    await message.answer(f"Salom, {message.from_user.full_name}!\n"
                         f"Botdan foydalanish uchun kontaktingizni yuboring.", reply_markup=phone)
    await state.set_state('phone')


@dp.message_handler(state='phone', content_types='contact', is_sender_contact=True, user_id=ADMINS)
async def send_contact_admin(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    fullname = msg.from_user.full_name
    phone_num = msg.contact.phone_number
    db.add_user(user_id, fullname, phone_num)
    await msg.answer("Botdan foydalanishingiz mumkin!", reply_markup=add_test_bot)
    await state.finish()


@dp.message_handler(state='phone', content_types='contact', is_sender_contact=True)
async def send_contact(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    fullname = msg.from_user.full_name
    phone_num = msg.contact.phone_number
    db.add_user(user_id, fullname, phone_num)
    info = "Foydalanuvchi qo'shildi!\n"
    info += f"id: {user_id}\n" \
            f"fullname: {fullname}\n" \
            f"phone number: {phone_num}"
    await msg.answer("Botdan foydalanishingiz mumkin!", reply_markup=test)
    await bot.send_message(ADMINS[0], info)
    await state.finish()


@dp.message_handler(state='phone', content_types=ContentType.ANY)
async def failed_send_phone(msg: types.Message, state: FSMContext):
    await msg.answer("Botdan foydalanish uchun kontaktingizni yuboring!", reply_markup=phone)

