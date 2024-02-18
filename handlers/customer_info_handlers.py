from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from database import DB
from messages import *
from keyboards import *
from states import CustomerInfoStatesGroup


async def change_customer_info(callback: types.CallbackQuery):
    await callback.message.answer(text=f'🔴 Ваше имя?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                                  reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.first_name.set()


async def save_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.answer(text=f'🔴 Ваша фамилия?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                         reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.next()


async def save_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.answer(text=f'🔴 Номер телефона?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                         reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.next()


async def save_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.answer(text=f'🔴 Ваш адрес для доставки?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                         reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.next()


async def save_delivery_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_address'] = message.text

    customer_info = [message.from_user.id, data['first_name'], data['last_name'],
                     data['phone_number'], data['delivery_address']]
    DB.change_customer_info(*customer_info)

    await message.answer(text=await get_customer_info_msg(customer_info), reply_markup=customer_info_ikb)
    await state.finish()


async def cancel_user_info_changes(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    customer_info = DB.get_customer(user_id=callback.from_user.id)
    await callback.message.answer(text=await get_customer_info_msg(customer_info), reply_markup=customer_info_ikb)


def register_customer_info_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(change_customer_info, text='Изменить пользователя')

    dp.register_message_handler(callback=save_first_name, state=CustomerInfoStatesGroup.first_name)
    dp.register_message_handler(callback=save_last_name, state=CustomerInfoStatesGroup.last_name)
    dp.register_message_handler(callback=save_phone_number, state=CustomerInfoStatesGroup.phone_number)
    dp.register_message_handler(callback=save_delivery_address, state=CustomerInfoStatesGroup.delivery_address)

    dp.register_callback_query_handler(callback=cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.first_name,
                                       text='Не изменять пользователя')

    dp.register_callback_query_handler(callback=cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.last_name,
                                       text='Не изменять пользователя')

    dp.register_callback_query_handler(callback=cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.phone_number,
                                       text='Не изменять пользователя')

    dp.register_callback_query_handler(callback=cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.delivery_address,
                                       text='Не изменять пользователя')
