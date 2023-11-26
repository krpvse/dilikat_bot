from aiogram import types, Dispatcher

from loader import bot, dp
from messages import *
from keyboards import *


async def show_material_product(message: types.Message):
    if '/id' in message.text:
        product_image = types.InputFile('files/product.png')
        await bot.send_photo(message.from_user.id, photo=product_image)
        await bot.send_message(chat_id=message.from_user.id, text=get_product_description_msg(),
                               reply_markup=product_ikb)
    await bot.delete_message(message.from_user.id, message.message_id-1)


async def choose_material_type(callback: types.CallbackQuery):
    if callback.data == 'Фотополимеры' or callback.data == 'CAD CAM блоки' or callback.data == 'Фрезы':
        await callback.message.answer(text=category_products_message, reply_markup=category_products_ikb)


def register_material_handlers(dp: Dispatcher):
    dp.register_message_handler(show_material_product)

    dp.register_callback_query_handler(choose_material_type)
