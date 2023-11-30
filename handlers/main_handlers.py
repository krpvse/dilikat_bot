from aiogram import types, Dispatcher

from loader import bot, db
from messages import *
from keyboards import *


async def start(message: types.Message):
    logo_img = types.InputFile('database/dilikat-logo.png')
    await bot.send_photo(message.from_user.id, photo=logo_img)
    await bot.send_message(message.from_user.id, hello_msg, reply_markup=main_ikb)

    db.add_user(message.from_user.id, message.from_user.username,
                message.from_user.first_name, message.from_user.last_name)
    await message.delete()


async def change_section(callback: types.CallbackQuery):
    if callback.data == 'Главное меню':
        logo_img = types.InputFile('database/dilikat-logo.png')
        await bot.send_photo(callback.from_user.id, photo=logo_img)
        await callback.message.answer(text=main_section_msg, reply_markup=main_ikb)

    if callback.data == 'Материалы':
        await callback.message.answer(text=materials_section_msg,
                                      reply_markup=materials_ikb)

    if callback.data == 'Оборудование':
        await callback.message.answer(text=equipment_section_msg,
                                      reply_markup=equipment_ikb)

    if callback.data == 'Мои данные':
        await callback.message.answer(text=get_customer_info_msg(callback.from_user.id),
                                      reply_markup=customer_info_ikb)

    if callback.data == 'Позвонить':
        await callback.message.answer(text=call_section_msg,
                                      reply_markup=call_ikb)

    if callback.data == 'Корзина':
        await callback.message.answer(text=get_basket_info_msg(callback.from_user.id),
                                      reply_markup=basket_ikb)


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_callback_query_handler(change_section)
