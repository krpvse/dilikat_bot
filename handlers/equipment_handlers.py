from aiogram import types, Dispatcher

from loader import bot, dp
from messages.messages import *
from keyboards import *


async def choose_equipment_type(callback: types.CallbackQuery):
    if callback.data == '3D принтеры' or callback.data == '3D сканеры' or callback.data == 'Печи' \
            or callback.data == 'Фрезерные станки':
        await callback.message.answer(text=category_products_message, reply_markup=category_products_ikb)


async def show_equipment_product(message: types.Message):
    if '/id' in message.text:
        product_image = types.InputFile('files/product.png')
        await bot.send_photo(message.from_user.id, photo=product_image)
        await bot.send_message(chat_id=message.from_user.id, text=get_product_description_msg(),
                               reply_markup=product_ikb)
    await bot.delete_message(message.from_user.id, message.message_id-1)


def register_equipment_handlers(dp: Dispatcher):
    dp.register_message_handler(show_equipment_product)

    dp.register_callback_query_handler(choose_equipment_type)
