from aiogram import types, Dispatcher

from loader import dp, db
from messages import *
from keyboards import *


async def add_product(callback: types.CallbackQuery):
    if callback.data == 'Добавить в корзину':
        db.add_basket_product(callback.from_user.id, 11111, 'Заголовок товара')
        await callback.answer(text=f'Добавили в корзину', show_alert=True)


async def remove_product(callback: types.CallbackQuery):
    if callback.data == 'Убрать из корзины':
        db.remove_basket_product(callback.from_user.id, 11111, 'Заголовок товара')
        await callback.answer(text=f'Убрали из корзины', show_alert=True)


def register_basket_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(add_product)
    dp.register_callback_query_handler(remove_product)
