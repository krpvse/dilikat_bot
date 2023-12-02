from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from loader import db, bot
from messages import *
from keyboards import *
from states import CustomerInfoStatesGroup


async def change_customer_info(callback: types.CallbackQuery):
    await callback.message.edit_text(text=change_first_name_msg, reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.first_name.set()


async def save_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    main_message_id = db.get_main_message_id(message.from_user.id)
    await bot.edit_message_text(text=change_last_name_msg, reply_markup=customer_info_change_ikb,
                                chat_id=message.from_user.id, message_id=main_message_id)
    await message.delete()
    await CustomerInfoStatesGroup.next()


async def save_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    main_message_id = db.get_main_message_id(message.from_user.id)
    await bot.edit_message_text(text=change_phone_number_msg, reply_markup=customer_info_change_ikb,
                                chat_id=message.from_user.id, message_id=main_message_id)
    await message.delete()
    await CustomerInfoStatesGroup.next()


async def save_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    main_message_id = db.get_main_message_id(message.from_user.id)
    await bot.edit_message_text(text=change_delivery_address_msg, reply_markup=customer_info_change_ikb,
                                chat_id=message.from_user.id, message_id=main_message_id)
    await message.delete()
    await CustomerInfoStatesGroup.next()


async def save_delivery_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_address'] = message.text

    db.change_customer_info(message.from_user.id, data['first_name'], data['last_name'],
                        data['phone_number'], data['delivery_address'])

    main_message_id = db.get_main_message_id(message.from_user.id)
    await bot.edit_message_text(text=get_customer_info_msg(message.from_user.id),
                                reply_markup=customer_info_ikb,
                                chat_id=message.from_user.id,
                                message_id=main_message_id)
    await message.delete()
    await state.finish()


async def cancel_user_info_changes(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    main_message_id = db.get_main_message_id(callback.from_user.id)
    await bot.edit_message_text(text=get_customer_info_msg(callback.from_user.id),
                                reply_markup=customer_info_ikb,
                                chat_id=callback.from_user.id,
                                message_id=main_message_id)


def register_customer_info_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(change_customer_info, text='Изменить пользователя')

    dp.register_message_handler(save_first_name, state=CustomerInfoStatesGroup.first_name)
    dp.register_message_handler(save_last_name, state=CustomerInfoStatesGroup.last_name)
    dp.register_message_handler(save_phone_number, state=CustomerInfoStatesGroup.phone_number)
    dp.register_message_handler(save_delivery_address, state=CustomerInfoStatesGroup.delivery_address)

    dp.register_callback_query_handler(cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.first_name,
                                       text='Не изменять пользователя')

    dp.register_callback_query_handler(cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.last_name,
                                       text='Не изменять пользователя')

    dp.register_callback_query_handler(cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.phone_number,
                                       text='Не изменять пользователя')

    dp.register_callback_query_handler(cancel_user_info_changes,
                                       state=CustomerInfoStatesGroup.delivery_address,
                                       text='Не изменять пользователя')
