from aiogram import types, Dispatcher

from loader import bot, catalog, db
from messages import *
from keyboards import *


product_ids = [f'id{product[0]}' for product in catalog]


async def show_category_products(callback: types.CallbackQuery):
    await callback.message.edit_text(text=get_category_products_msg(callback.data),
                                     reply_markup=category_products_ikb)


async def show_product(message: types.Message):
    # delete old main_messages if exists
    old_main_message_id = db.get_main_message_id(message.from_user.id)
    if old_main_message_id:
        await bot.delete_message(message.from_user.id, old_main_message_id)
        await bot.delete_message(message.from_user.id, old_main_message_id-1)

    # save new main_message_id
    db.save_main_message_id(message.from_user.id, message.message_id+2)

    # send product message
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
