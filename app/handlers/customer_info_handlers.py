from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from pydantic import ValidationError

from logs import bot_logger as logger
from database import DB
from messages import get_customer_info_msg
from keyboards import customer_info_change_ikb, customer_info_ikb
from states import CustomerInfoStatesGroup
from database.schemas.input_schemas import CustomerInfoSchema


async def change_customer_info(callback: types.CallbackQuery):
    logger.info(f'User {callback.from_user.id} is changing customer info')
    await callback.message.answer(text=f'🔴 Ваше имя?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                                  reply_markup=customer_info_change_ikb)
    await CustomerInfoStatesGroup.first_name.set()


async def save_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    try:
        validated_first_name = CustomerInfoSchema(first_name=first_name)
    except ValidationError as e:
        validated_first_name = None
        logger.info(f'User {message.from_user.id} write WRONG name "{first_name}"\nDetails: {e}')

    if validated_first_name:
        async with state.proxy() as data:
            data['first_name'] = first_name
        logger.info(f'User {message.from_user.id} write first name {first_name}')

        await message.answer(text=f'🔴 Ваша фамилия?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)
        await CustomerInfoStatesGroup.next()
    else:
        await message.answer(text=f'В вашем имени совсем нет букв?\n\n<i>Введите, пожалуйста, имя с буквами</i>',
                             reply_markup=customer_info_change_ikb)


async def save_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    try:
        validated_last_name = CustomerInfoSchema(last_name=last_name)
    except ValidationError as e:
        validated_last_name = None
        logger.info(f'User {message.from_user.id} write WRONG name "{last_name}"\nDetails: {e}')

    if validated_last_name:
        async with state.proxy() as data:
            data['last_name'] = last_name
        logger.info(f'User {message.from_user.id} write last name {last_name}')

        await message.answer(text=f'🔴 Номер телефона?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)
        await CustomerInfoStatesGroup.next()
    else:
        await message.answer(text=f'В вашей фамилии совсем нет букв?\n\n<i>Введите, пожалуйста, фамилию с буквами</i>',
                             reply_markup=customer_info_change_ikb)


async def save_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    try:
        validated_phone_number = CustomerInfoSchema(phone_number=phone_number)
    except ValidationError as e:
        validated_phone_number = None
        logger.info(f'User {message.from_user.id} write WRONG phone number "{phone_number}"\nDetails: {e}')

    if validated_phone_number:
        async with state.proxy() as data:
            data['phone_number'] = phone_number
        logger.info(f'User {message.from_user.id} write phone number {phone_number}')

        await message.answer(text=f'🔴 Ваш адрес для доставки?\n\n<i>Напишите в одном сообщении, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)
        await CustomerInfoStatesGroup.next()
    else:
        await message.answer(text=f'Маловато цифр в номере телефона\n\n<i>Напишите, пожалуйста, номер с большим количеством цифр</i>',
                             reply_markup=customer_info_change_ikb)


async def save_delivery_address(message: types.Message, state: FSMContext):
    address = message.text
    try:
        validated_address = CustomerInfoSchema(delivery_address=address)
    except ValidationError as e:
        validated_address = None
        logger.info(f'User {message.from_user.id} write WRONG address "{address}"\nDetails: {e}')

    if validated_address:
        async with state.proxy() as data:
            data['delivery_address'] = message.text
        logger.info(f'User {message.from_user.id} write address {address}')

        await DB.change_customer_info(user_id=message.from_user.id, first_name=data['first_name'], last_name=data['last_name'],
                                phone_number=data['phone_number'], delivery_address=data['delivery_address'])

        customer_info = await DB.get_customer_info(user_id=message.from_user.id)
        await message.answer(text=get_customer_info_msg(customer_info), reply_markup=customer_info_ikb)
        await state.finish()
        logger.info(f'User {message.from_user.id} succesfully completed customer info changing')
    else:
        await message.answer(text=f'Маловато букв в адресе. Должно быть как минимум 5 букв\n\n<i>Напишите подробнее, пожалуйста</i>',
                             reply_markup=customer_info_change_ikb)


async def cancel_user_info_changes(callback: types.CallbackQuery, state: FSMContext):
    logger.info(f'User {callback.from_user.id} canceled customer info changing')
    await state.finish()

    customer_info = await DB.get_customer_info(user_id=callback.from_user.id)
    await callback.message.answer(text=get_customer_info_msg(customer_info), reply_markup=customer_info_ikb)


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
