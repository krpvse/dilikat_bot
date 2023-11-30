from aiogram import types, Dispatcher

from loader import db
from messages import *
from keyboards import *


async def add_product(callback: types.CallbackQuery):
    db.add_basket_product(callback.from_user.id, 202)
    await callback.answer(text=f'Добавили в корзину', show_alert=True)


async def remove_product(callback: types.CallbackQuery):
    db.remove_basket_product(callback.from_user.id, 202)
    await callback.answer(text=f'Убрали из корзины', show_alert=True)


async def create_order(callback: types.CallbackQuery):
    db.create_order(callback.from_user.id)
    db.remove_customer_basket(callback.from_user.id)

    await callback.answer(text=f'Заявка отправлена!', show_alert=True)
    await callback.message.answer(text=main_section_msg, reply_markup=main_ikb)


def register_basket_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback=add_product, text=['Добавить в корзину'])
    dp.register_callback_query_handler(callback=remove_product, text=['Убрать из корзины'])
    dp.register_callback_query_handler(callback=create_order, text=['Оформить заказ'])
