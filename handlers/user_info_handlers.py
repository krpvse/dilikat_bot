from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from loader import dp, db
from messages.messages import *
from keyboards import *
from states import UserInfoStatesGroup


async def save_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await UserInfoStatesGroup.next()
    await message.answer(text=change_last_name_msg, reply_markup=user_info_change_ikb)


async def save_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await UserInfoStatesGroup.next()
    await message.answer(text=change_phone_number_msg, reply_markup=user_info_change_ikb)


async def save_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await UserInfoStatesGroup.next()
    await message.answer(text=change_delivery_address_msg, reply_markup=user_info_change_ikb)


async def save_delivery_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_address'] = message.text
    await state.finish()

    db.change_user_info(message.from_user.id, data['first_name'], data['last_name'],
                        data['phone_number'], data['delivery_address'])
    await message.answer(text=get_user_info_msg(message.from_user.id), reply_markup=user_info_ikb)


async def cancel_user_info_changes(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Не изменять данные':
        await state.finish()
        await callback.message.answer(text=get_user_info_msg(callback.from_user.id),
                                      reply_markup=user_info_ikb)


def register_user_info_handlers(dp: Dispatcher):
    dp.register_message_handler(save_first_name, state=UserInfoStatesGroup.first_name)
    dp.register_message_handler(save_last_name, state=UserInfoStatesGroup.last_name)
    dp.register_message_handler(save_phone_number, state=UserInfoStatesGroup.phone_number)
    dp.register_message_handler(save_delivery_address, state=UserInfoStatesGroup.delivery_address)

    dp.register_callback_query_handler(cancel_user_info_changes, state=UserInfoStatesGroup.first_name)
    dp.register_callback_query_handler(cancel_user_info_changes, state=UserInfoStatesGroup.last_name)
    dp.register_callback_query_handler(cancel_user_info_changes, state=UserInfoStatesGroup.phone_number)
    dp.register_callback_query_handler(cancel_user_info_changes, state=UserInfoStatesGroup.delivery_address)
