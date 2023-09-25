from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default import test
from keyboards.inline import full_signup, confirm
from loader import dp, db, bot
from states import FullSignupState


@dp.callback_query_handler(text=('full_signup', 'false'), state=(FullSignupState.register, FullSignupState.confirm))
async def full_register(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Emailingizni kiriting: ")
    await state.set_state(FullSignupState.email)


@dp.message_handler(content_types=ContentType.ANY, state=FullSignupState.register)
async def err_full_signup(msg: types.Message, state: FSMContext):
    await msg.answer("Iltimos ro'yxatdan o'tish uchun tugmani bosing!")


@dp.message_handler(state=FullSignupState.email)
async def send_email(msg: types.Message, state: FSMContext):
    await state.update_data({'email': msg.text})
    await msg.answer("Tug'ilgan kuningizni kiriting\n"
                     "Tartibi (12-12-2000 yoki 12.12.2000): ")
    await FullSignupState.next()


@dp.message_handler(state=FullSignupState.birthday)
async def send_birthday(msg: types.Message, state: FSMContext):
    birthday = msg.text.replace('.', '-')
    await state.update_data({'birthday': birthday})
    async with state.proxy() as data:
        email = data['email']
        birthday = data['birthday']
        db.add_email_birthday(msg.from_user.id, f"{email}", f"{birthday}")
    info = "Ma'lumotlaringiz to'g'ri ekanligini tasdiqlang!\n"
    user = db.select_user(msg.from_user.id)
    info += f"Ism-familiyangiz: {user[1]}\n" \
            f"Telefon nomeringiz: {user[2]}\n" \
            f"Emailingiz: {user[3]}\n" \
            f"Tug'ilgan kuningiz: {user[4]}"
    await msg.answer(info, reply_markup=confirm)
    await bot.send_message(ADMINS[0], info)
    await FullSignupState.next()


@dp.callback_query_handler(text='true', state=FullSignupState.confirm)
async def confirm_true(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Ma'lumotlaringiz muvaffaqqiyatli saqlandi!", show_alert=True)
    await call.message.answer("Test yechish tugmasini bosing", reply_markup=test)
    await call.message.delete()
    await state.finish()


@dp.message_handler(content_types=ContentType.ANY, state=FullSignupState.confirm)
async def any_message(msg: types.Message):
    await msg.answer("Ma'lumotlaringiz to'g'ri ekanligini tasdiqlang!")



