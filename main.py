from aiogram import Bot, Dispatcher, executor, types

from config import test_bot_token
from keyboards import categories_ikb, main_ikb, product_ikb, category_products_ikb, user_info_ikb
from messages import product_message, category_products_message, get_user_info_message
import database as db

bot = Bot(token=test_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    hello_image = types.InputFile('files/hello_image.png')
    await bot.send_photo(message.from_user.id, photo=hello_image)
    await bot.send_message(message.from_user.id,
                           '👋 Привет! Это бот для заказов Dilikat\nЗдесь вы можете оставить заявку, '
                           'а наши менеджеры оперативно её обработают',
                           parse_mode='HTML',
                           reply_markup=main_ikb)
    db.add_user(message.from_user.id, message.from_user.username,
                message.from_user.first_name, message.from_user.last_name)


@dp.callback_query_handler()
async def change_section(callback: types.CallbackQuery):
    if callback.data == 'Категории продуктов':
        await callback.message.answer(text='🔴 Что вас интересует?',
                                      reply_markup=categories_ikb)
    if callback.data == 'Мои данные':
        await callback.message.answer(text=get_user_info_message(callback.from_user.id),
                                      reply_markup=user_info_ikb,
                                      parse_mode='HTML')
    if callback.data == 'Главное меню':
        await callback.message.answer(text='🔴 Вы в главном меню бота. Сделаем заказ?',
                                      reply_markup=main_ikb,
                                      parse_mode='HTML')
    if callback.data == 'Изменить данные пользователя':
        await callback.message.answer(text='🔴 Вы в главном меню бота. Сделаем заказ?',
                                      reply_markup=main_ikb,
                                      parse_mode='HTML')

    if callback.data == '3D принтеры' or callback.data == '3D сканеры' or callback.data == 'Печи' \
            or callback.data == 'Фрезерные станки' or callback.data == 'Фотополимеры' or callback.data == 'CAD CAM блоки':
        await callback.message.answer(text=category_products_message,
                                      reply_markup=category_products_ikb,
                                      parse_mode='HTML')


@dp.message_handler()
async def show_product(message: types.Message):
    if '/id' in message.text:
        product_image = types.InputFile('files/product.png')
        await bot.send_photo(message.from_user.id, photo=product_image)
        await bot.send_message(chat_id=message.from_user.id,
                               text=product_message,
                               parse_mode='HTML',
                               reply_markup=product_ikb)
    await bot.delete_message(message.from_user.id, message.message_id-1)


@dp.message_handler()
async def delete_other_messages(message: types.Message):
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
















# @dp.message_handler(commands=['choose_category'])
# async def start(message: types.Message):
#     await message.delete()
#     await bot.send_message(message.from_user.id,
#                            '<b>🔴 Выберите категорию товара:</b>',
#                            reply_markup=category_ikb,
#                            parse_mode='HTML')


# @dp.message_handler(commands=['make_order'])
# async def start(message: types.Message):
#     await message.delete()
#     await bot.send_message(message.from_user.id, 'Давайте запишем ваши данные, чтобы не спрашивать каждый раз!')
#     await bot.send_message(message.from_user.id, '<b>🔴 Напишите ваше имя</b>', parse_mode='HTML')
#     await bot.send_message(message.from_user.id, '<b>🔴 Теперь напишите фамилию</b>', parse_mode='HTML')


#reply - ответ на сообщение,