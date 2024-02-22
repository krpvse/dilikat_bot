from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from database import DB
from messages import *
from keyboards import *
from states import CustomerInfoStatesGroup
from utils.validators import validate_name, validate_phone_number, validate_delivery_address


async def change_customer_info(callback: types.CallbackQuery):
    await callback.message.answer(text=f'🔴 Ваше имя?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                                  reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.first_name.set()


async def save_first_name(message: types.Message, state: FSMContext):
    first_name = await validate_name(message.text)

    if first_name:
        async with state.proxy() as data:
            data['first_name'] = first_name
        await message.answer(text=f'🔴 Ваша фамилия?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)
        await CustomerInfoStatesGroup.next()
    else:
        await message.answer(text=f'В вашем имени совсем нет букв?\n\n <i>Введите, пожалуйста, имя с буквами</i>',
                             reply_markup=customer_info_change_ikb)


async def save_last_name(message: types.Message, state: FSMContext):
    last_name = await validate_name(message.text)

    if last_name:
        async with state.proxy() as data:
            data['last_name'] = last_name
        await message.answer(text=f'🔴 Номер телефона?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)
        await CustomerInfoStatesGroup.next()
    else:
        await message.answer(text=f'В вашей фамилии совсем нет букв?\n\n <i>Введите, пожалуйста, фамилию с буквами</i>',
                             reply_markup=customer_info_change_ikb)


async def save_phone_number(message: types.Message, state: FSMContext):
    phone_number = await validate_phone_number(message.text)

    if phone_number:
        async with state.proxy() as data:
            data['phone_number'] = phone_number
        await message.answer(text=f'🔴 Ваш адрес для доставки?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)
        await CustomerInfoStatesGroup.next()
    else:
        await message.answer(text=f'Маловато цифр в номере телефона\n\n <i>Напишите, пожалуйста, номер с большим количеством цифр</i>',
                             reply_markup=customer_info_change_ikb)


async def save_delivery_address(message: types.Message, state: FSMContext):
    address = await validate_delivery_address(message.text)

    if address:
        async with state.proxy() as data:
            data['delivery_address'] = message.text

        DB.change_customer_info(user_id=message.from_user.id, first_name=data['first_name'], last_name=data['last_name'],
                                phone_number=data['phone_number'], delivery_address=data['delivery_address'])

        customer_info = DB.get_customer_info(user_id=message.from_user.id)
        await message.answer(text=await get_customer_info_msg(customer_info), reply_markup=customer_info_ikb)
        await state.finish()
    else:
        await message.answer(text=f'Маловато букв в адресе. Должно быть как минимум 5 букв\n\n <i>Напишите подробнее, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)


async def cancel_user_info_changes(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    customer_info = DB.get_customer_info(user_id=callback.from_user.id)
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
