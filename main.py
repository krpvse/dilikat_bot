from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config import bot_token
from keyboards import main_ikb, equipment_ikb, materials_ikb, product_ikb, user_info_ikb, call_ikb, basket_ikb, \
    category_products_ikb, user_info_change_ikb
from messages import *
from database import Database


bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    hello_image = types.InputFile('files/logo.png')
    await bot.send_photo(message.from_user.id, photo=hello_image)

    await bot.send_message(message.from_user.id, hello_msg, reply_markup=main_ikb, parse_mode='HTML')

    db.add_user(message.from_user.id, message.from_user.username,
                message.from_user.first_name, message.from_user.last_name)


@dp.callback_query_handler()
async def change_section(callback: types.CallbackQuery):
    if callback.data == 'Главное меню':
        hello_image = types.InputFile('files/logo.png')
        await bot.send_photo(callback.from_user.id, photo=hello_image)
        await callback.message.answer(text=main_section_msg, reply_markup=main_ikb, parse_mode='HTML')

    if callback.data == 'Материалы':
        await callback.message.answer(text=materials_section_msg, reply_markup=materials_ikb)

    if callback.data == 'Оборудование':
        await callback.message.answer(text=equipment_section_msg, reply_markup=equipment_ikb)

    if callback.data == 'Мои данные':
        await callback.message.answer(text=get_user_info_msg(callback.from_user.id),
                                      reply_markup=user_info_ikb,
                                      parse_mode='HTML')

    if callback.data == 'Позвонить':
        await callback.message.answer(text=call_section_msg, reply_markup=call_ikb,)

    if callback.data == 'Добавить в корзину':
        db.add_basket_product(callback.from_user.id, 11111, 'Заголовок товара')
        await callback.answer(text=f'Добавили в корзину',
                              show_alert=True)

    if callback.data == 'Убрать из корзины':
        db.remove_basket_product(callback.from_user.id, 11111, 'Заголовок товара')
        await callback.answer(text=f'Убрали из корзины',
                              show_alert=True)

    if callback.data == 'Корзина':
        await callback.message.answer(text=get_basket_info_msg(callback.from_user.id),
                                      reply_markup=basket_ikb,
                                      parse_mode='HTML')

    if callback.data == '3D принтеры' or callback.data == '3D сканеры' or callback.data == 'Печи' \
            or callback.data == 'Фрезерные станки' or callback.data == 'Фотополимеры' or callback.data == 'CAD CAM блоки'\
            or callback.data == 'Фрезы':
        await callback.message.answer(text=category_products_message,
                                      reply_markup=category_products_ikb,
                                      parse_mode='HTML')

    if callback.data == 'Назад':
        await callback.answer(text='В разработке', show_alert=True)

    if callback.data == 'Изменить данные пользователя':
        await ClientStatesGroup.first_name.set()
        await callback.message.answer(text=change_first_name_msg,
                                      reply_markup=user_info_change_ikb,
                                      parse_mode='HTML')


@dp.message_handler()
async def show_product(message: types.Message):
    if '/id' in message.text:
        product_image = types.InputFile('files/product.png')
        await bot.send_photo(message.from_user.id, photo=product_image)
        await bot.send_message(chat_id=message.from_user.id,
                               text=get_product_description_msg(),
                               parse_mode='HTML',
                               reply_markup=product_ikb)
    await bot.delete_message(message.from_user.id, message.message_id-1)


@dp.message_handler()
async def delete_other_messages(message: types.Message):
    await message.delete()


# ------------------------------------------Change user info

class ClientStatesGroup(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    delivery_address = State()


@dp.message_handler(state=ClientStatesGroup.first_name)
async def save_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await ClientStatesGroup.next()
    await message.answer(text=change_last_name_msg,
                         reply_markup=user_info_change_ikb,
                         parse_mode='HTML')


@dp.message_handler(state=ClientStatesGroup.last_name)
async def save_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await ClientStatesGroup.next()
    await message.answer(text=change_phone_number_msg,
                         reply_markup=user_info_change_ikb,
                         parse_mode='HTML')


@dp.message_handler(state=ClientStatesGroup.phone_number)
async def save_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await ClientStatesGroup.next()
    await message.answer(text=change_delivery_address_msg,
                         reply_markup=user_info_change_ikb,
                         parse_mode='HTML')


@dp.message_handler(state=ClientStatesGroup.delivery_address)
async def save_delivery_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_address'] = message.text
    await state.finish()
    db.change_user_info(message.from_user.id, data['first_name'], data['last_name'],
                        data['phone_number'], data['delivery_address'])
    await message.answer(text=get_user_info_msg(message.from_user.id),
                         reply_markup=user_info_ikb,
                         parse_mode='HTML')


@dp.callback_query_handler(state=ClientStatesGroup.first_name)
@dp.callback_query_handler(state=ClientStatesGroup.last_name)
@dp.callback_query_handler(state=ClientStatesGroup.phone_number)
@dp.callback_query_handler(state=ClientStatesGroup.delivery_address)
async def change_section(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Не изменять данные':
        await state.finish()
        await callback.message.answer(text=get_user_info_msg(callback.from_user.id),
                                      reply_markup=user_info_ikb,
                                      parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
