from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("info", "Profilim ma'lumotlari"),
            types.BotCommand("set_fullname", "Ism-familiyani o'zgartirish"),
            types.BotCommand("set_email", "Emailni o'zgartirish"),
            types.BotCommand("set_number", "Telefon raqamni o'zgartirish"),
            types.BotCommand("set_birthday", "Tug'ilgan kunni o'zgartirish"),
            types.BotCommand("all_users", "Barcha foydalanuvchilar"),
            types.BotCommand("send_post", "Barcha foydalanuvchilarga post yuborish"),
            types.BotCommand("del_tests", "Barcha testlarni o'chirish"),
            types.BotCommand("del_users", "Barcha foydalanuvchilarni o'chirish"),
        ]
    )
