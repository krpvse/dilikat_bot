from aiogram import types, Dispatcher

from loader import bot, db
from messages import *
from keyboards import *


async def start(message: types.Message):
    # delete old main_messages if exists
    old_main_message_id = db.get_main_message_id(message.from_user.id)
    if old_main_message_id:
        await bot.delete_message(message.from_user.id, old_main_message_id-1)
        await bot.delete_message(message.from_user.id, old_main_message_id)

    # add user info
    db.add_user(message.from_user.id, message.from_user.username,
                message.from_user.first_name, message.from_user.last_name)

    # save new main_message_id
    db.save_main_message_id(message.from_user.id, message.message_id+2)

    # send start message
    logo_img = types.InputFile('database/dilikat-logo.png')
    await bot.send_photo(message.from_user.id, photo=logo_img)
    await bot.send_message(message.from_user.id, hello_msg, reply_markup=main_ikb)
    await message.delete()


async def change_section(callback: types.CallbackQuery):
    if callback.data == 'Главное меню':
        await callback.message.edit_text(text=main_section_msg, reply_markup=main_ikb)

    if callback.data == 'Материалы':
        await callback.message.edit_text(text=materials_section_msg, reply_markup=materials_ikb)

    if callback.data == 'Оборудование':
        await callback.message.edit_text(text=equipment_section_msg, reply_markup=equipment_ikb)

    if callback.data == 'Мои данные':
        await callback.message.edit_text(text=get_customer_info_msg(callback.from_user.id),
                                         reply_markup=customer_info_ikb)

    if callback.data == 'Позвонить':
        await callback.message.edit_text(text=call_section_msg, reply_markup=call_ikb)

    if callback.data == 'Корзина':
        await callback.message.edit_text(text=get_basket_info_msg(callback.from_user.id),
                                         reply_markup=basket_ikb)


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_callback_query_handler(change_section)
