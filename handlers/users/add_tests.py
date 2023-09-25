import asyncio
import sqlite3
from datetime import datetime

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from keyboards.default import add_test_bot

from data.config import ADMINS
from keyboards.default import skip_button
from keyboards.inline import confirm
from loader import dp, db
from states import TestStateGroup


@dp.message_handler(text="📥 Test qo'shish", user_id=ADMINS)
async def add_test(msg: types.Message, state: FSMContext):
    await msg.answer("Testning rasmi bo'lsa, rasmni yuboring aks holda o'tkazib yuborish!", reply_markup=skip_button)
    await TestStateGroup.photo.set()


@dp.message_handler(content_types=(ContentType.PHOTO, ContentType.DOCUMENT), state=TestStateGroup.photo)
async def send_photo(msg: types.Message, state: FSMContext):
    if msg.photo:
        doc_id = msg.photo[-1].file_id
    else:
        doc_id = msg.document.file_id
    await state.update_data({'doc_id': doc_id})
    await msg.answer("Test shartini kiriting (majburiy): ", reply_markup=ReplyKeyboardRemove())
    await TestStateGroup.next()


@dp.message_handler(text="⏭ O'tkazib yuborish", state=TestStateGroup.photo)
async def skip(msg: types.Message):
    await msg.answer("Test shartini kiriting (majburiy): ", reply_markup=ReplyKeyboardRemove())
    await TestStateGroup.next()


@dp.message_handler(content_types=ContentType.ANY, state=TestStateGroup.photo)
async def error_photo(msg: types.Message):
    await msg.answer("Rasm yuboring yoki o'tkazib yuborish tugmasini bosing!", reply_markup=skip_button)


@dp.message_handler(state=TestStateGroup.question)
async def send_question(msg: types.Message, state: FSMContext):
    await state.update_data({'question': msg.text})
    await msg.answer("1-variantni kiriting va u to'g'ri javob bo'lsin:")
    await TestStateGroup.next()


@dp.message_handler(state=TestStateGroup.response)
async def send_true_response(msg: types.Message, state: FSMContext):
    await state.update_data({'response': msg.text})
    await msg.answer("2-variantni kiriting: ")
    await TestStateGroup.next()


@dp.message_handler(state=TestStateGroup.response1)
async def send_two_response(msg: types.Message, state: FSMContext):
    await state.update_data({'response1': msg.text})
    await msg.answer("3-variantni kiriting: ")
    await TestStateGroup.next()


@dp.message_handler(state=TestStateGroup.response2)
async def send_three_response(msg: types.Message, state: FSMContext):
    await state.update_data({'response2': msg.text})
    await msg.answer("4-variantni kiriting: ")
    await TestStateGroup.next()


@dp.message_handler(state=TestStateGroup.response3)
async def send_four_response(msg: types.Message, state: FSMContext):
    await state.update_data({'response3': msg.text})
    info = f"Test {datetime.now().date()} {datetime.now().strftime('%X')}:\n"
    async with state.proxy() as data:
        try:
            photo_id = data['doc_id']
        except KeyError:
            photo_id = None
        question = data['question']
        response = data['response']
        response1 = data['response1']
        response2 = data['response2']
        response3 = data['response3']
    info += f"Savol:\n" \
            f"{question}\n" \
            f"variant1*: {response}\n" \
            f"variant2: {response1}\n" \
            f"variant3: {response2}\n" \
            f"variant4: {response3}\n"
    if photo_id:
        try:
            await msg.answer_photo(photo_id, caption=info, reply_markup=confirm)
        except BadRequest:
            await msg.answer_document(photo_id, caption=info, reply_markup=confirm)
    else:
        await msg.answer(info, reply_markup=confirm)
    await TestStateGroup.next()


@dp.callback_query_handler(text='true', state=TestStateGroup.confirm)
async def confirm_true(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            photo_id = data['doc_id']
        except KeyError:
            photo_id = None
        question = data['question']
        response = data['response']
        response1 = data['response1']
        response2 = data['response2']
        response3 = data['response3']
    try:
        db.add_test(question, response, response1, response2, response3, photo_id)
    except sqlite3.IntegrityError:
        await call.message.delete()
        await call.message.answer("Bunday savol mavjud qayta kiriting:", reply_markup=add_test_bot)
        await state.finish()
        return
    await call.message.answer("Kategoriyani tanlang", reply_markup=add_test_bot)
    await call.answer("Test muvaffaqiyatli saqlandi!", show_alert=True)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='false', state=TestStateGroup.confirm)
async def confirm_true(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Qayta ma'lumotlarni kiriting!")
    await call.message.delete()
    await call.message.answer("Testning rasmi bo'lsa, rasmni yuboring aks holda o'tkazib yuborish!", reply_markup=skip_button)
    await TestStateGroup.photo.set()


@dp.message_handler(content_types=ContentType.ANY, state=TestStateGroup.confirm)
async def any_message(msg: types.Message):
    await msg.answer("Test to'g'ri ekanligini tasdiqlang!")


@dp.message_handler(text="🗒 Testlarni ko'rish", user_id=ADMINS)
async def add_test(msg: types.Message):
    tests = db.select_tests()
    count = db.select_count_tests()
    for test in tests:
        info = f"Test {test[6]}:\n"
        info += f"Savol:\n" \
                f"{test[0]}\n" \
                f"variant1*: {test[2]}\n" \
                f"variant2: {test[3]}\n" \
                f"variant3: {test[4]}\n" \
                f"variant4: {test[5]}\n"
        try:
            await msg.answer_photo(test[1], caption=info)
        except BadRequest:
            try:
                await msg.answer_document(test[1], caption=info)
            except BadRequest:
                await msg.answer(info)
        await asyncio.sleep(0.05)
    await msg.answer(f"Testlar soni: {count}")


