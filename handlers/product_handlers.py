from aiogram import types, Dispatcher

from loader import bot, catalog
from messages import *
from keyboards import *


product_ids = [f'id{product[0]}' for product in catalog]


async def show_category_products(callback: types.CallbackQuery):
    await callback.message.answer(text=get_category_products_msg(callback.data),
                                  reply_markup=category_products_ikb)


async def show_product(message: types.Message):
    product_id = int(message.text.replace('/id', ''))
    product_image_url = [product[3] for product in catalog if product_id in product][0]

    product_image = types.InputFile(f'database/{product_image_url}')
    await bot.send_photo(message.from_user.id, photo=product_image)

    await bot.send_message(chat_id=message.from_user.id,
                           text=get_product_msg(product_id),
                           reply_markup=product_ikb,
                           disable_web_page_preview=True)
    await message.delete()


def register_product_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback=show_category_products,
                                       text=['3D принтеры', '3D сканеры', 'Фрезерные станки', 'Печи',
                                             'CAD CAM блоки', 'Фрезы', 'Фотополимеры'])

    dp.register_message_handler(show_product, commands=product_ids)
