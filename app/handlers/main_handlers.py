import asyncio
from aiogram import types, Dispatcher

from logs import bot_logger as logger
from config import admin_id
from loader import bot
from database import DB
from messages import get_customer_info_msg, get_basket_msg, bot_info_msg
from keyboards import main_ikb, materials_ikb, equipment_ikb, customer_info_ikb, call_ikb, get_basket_ikb


async def start(message: types.Message):
    logger.info(f'User {message.from_user.id}-{message.from_user.username}-{message.from_user.full_name} started bot')
    asyncio.create_task(DB.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    ))

    logo_img = types.InputFile('database/logo.png')
    await message.answer_photo(photo=logo_img)
    await message.answer(text='👋 Привет! Это бот для заказов Dilikat\nЗдесь вы можете оставить заявку, а наши менеджеры'
                         ' оперативно её обработают.\n\n🔴 Что вас интересует?', reply_markup=main_ikb)
    await message.delete()


async def change_section(callback: types.CallbackQuery):
    if callback.data == 'Главное меню':
        logo_img = types.InputFile('database/logo.png')
        await callback.message.answer_photo(photo=logo_img)
        await callback.message.answer(text='🔴 Вы в главном меню бота. Хотите сделать заказ?', reply_markup=main_ikb)

    if callback.data == 'Материалы':
        await callback.message.answer(text='🔴 Какие расходные материалы интересуют?', reply_markup=materials_ikb)

    if callback.data == 'Оборудование':
        await callback.message.answer(text='🔴 Какое оборудование интересует?', reply_markup=equipment_ikb)

    if callback.data == 'Мои данные':
        customer_info = await DB.get_customer_info(user_id=callback.from_user.id)
        await callback.message.answer(text=get_customer_info_msg(customer_info), reply_markup=customer_info_ikb)

    if callback.data == 'Позвонить':
        await callback.message.answer(text='🔴 Наш номер: 88003018733\nНабирайте скорей, мы ждем 😉',
                                      reply_markup=call_ikb)

    if callback.data == 'Корзина':
        basket = await DB.get_basket(user_id=callback.from_user.id)
        await callback.message.answer(text=get_basket_msg(basket), reply_markup=get_basket_ikb(basket))


async def delete_other_messages(message: types.Message):
    logger.info(f'User {message.from_user.id} send unexpected message {message.text}')
    await bot.send_message(chat_id=admin_id, text=f'[ADMIN] Пользователь написал вне сценария: {message.text}\n\n'
                                                  f'id:{message.from_user.id}///{message.from_user.full_name}')
    await message.delete()


async def get_bot_info(message: types.Message):
    await message.answer(text=bot_info_msg)
    await message.delete()


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(get_bot_info, commands=['help'])
    dp.register_message_handler(delete_other_messages)

    dp.register_callback_query_handler(callback=change_section, text=['Главное меню', 'Материалы', 'Оборудование',
                                                                      'Мои данные', 'Позвонить', 'Корзина'])
