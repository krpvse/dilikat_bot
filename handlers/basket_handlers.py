from aiogram import types, Dispatcher

from database import DB
from messages import *
from keyboards import *


async def edit_basket_product_from_products(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if 'Добавить в корзину' in callback.data:
        product_id = int(callback.data.replace('Добавить в корзину ', ''))
        DB.add_to_basket(product_id=product_id, user_id=user_id)
        await callback.answer(text='Добавили в корзину', show_alert=True)
    else:
        product_id = int(callback.data.replace('Убрать из корзины ', ''))
        DB.remove_from_basket(product_id=product_id, user_id=user_id)
        await callback.answer(text='Убрали из корзины', show_alert=True)


async def edit_basket_product_from_basket(message: types.Message):
    user_id = message.from_user.id
    if 'add_id' in message.text:
        product_id = int(message.text.replace('/add_id', ''))
        DB.add_to_basket(product_id=product_id, user_id=user_id)
    else:
        product_id = int(message.text.replace('/rem_id', ''))
        DB.remove_from_basket(product_id=product_id, user_id=user_id)

    basket = DB.get_basket(user_id=user_id)
    await message.answer(text=await get_basket_msg(basket), reply_markup=await get_basket_ikb(basket))


async def clear_basket(callback: types.CallbackQuery):
    DB.clear_basket(user_id=callback.from_user.id)
    await callback.answer(text=f'Все товары удалены из корзины', show_alert=True)
    await callback.message.answer(text=await get_basket_msg(basket=None),
                                  reply_markup=await get_basket_ikb(basket=None))


async def create_order(callback: types.CallbackQuery):
    basket = DB.get_basket(user_id=callback.from_user.id)

    # ФУНКЦИОНАЛ ОТПРАВКИ УВЕДОМЛЕНИЙ О НОВОМ ЗАКАЗЕ

    await callback.answer(text=f'Заявка отправлена! Скоро с вами свяжется наш менеджер', show_alert=True)

    logo_img = types.InputFile('database/logo.png')
    await callback.message.answer_photo(photo=logo_img)
    await callback.message.edit_text(text='🔴 Вы в главном меню бота. Хотите сделать заказ?', reply_markup=main_ikb)


def register_basket_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback=edit_basket_product_from_products,
                                       text_startswith=['Добавить в корзину', 'Убрать из корзины'])

    dp.register_message_handler(callback=edit_basket_product_from_basket, text_startswith=['/add_id', '/rem_id'])
    dp.register_callback_query_handler(callback=clear_basket, text=['Очистить корзину'])
    dp.register_callback_query_handler(callback=create_order, text=['Оформить заказ'])
