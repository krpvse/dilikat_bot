import asyncio

from aiogram import types, Dispatcher

from logs import bot_logger as logger
from database import DB
from messages import get_basket_msg, get_customer_info_msg
from keyboards import get_basket_ikb, check_customer_info_ikb, customer_info_ikb, main_ikb
from utils.notifications import OrderTelegramNotification, OrderEmailNotification


async def edit_basket_product_from_products(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if 'Добавить в корзину' in callback.data:
        product_id = int(callback.data.replace('Добавить в корзину ', ''))

        # CHECK PRODUCT QUANTITY IN BASKET, MUST BE <= 10
        basket = await DB.get_basket(user_id=user_id)
        if len(basket) <= 10:
            asyncio.create_task(DB.add_to_basket(product_id=product_id, user_id=user_id))
            await callback.answer(text='Добавили в корзину', show_alert=True)
            logger.info(f'User {callback.from_user.id} add product id{product_id} in basket')

        else:
            await callback.answer(
                text='Много товаров в корзине. Удалите что-то, или звоните нам, чтобы сделать такой большой заказ!',
                show_alert=True
            )
            logger.info(f'User {callback.from_user.id} cannot add product id{product_id} in basket, there is max qty')

    elif 'Убрать из корзины' in callback.data:
        product_id = int(callback.data.replace('Убрать из корзины ', ''))
        asyncio.create_task(DB.remove_from_basket(product_id=product_id, user_id=user_id))
        await callback.answer(text='Убрали из корзины', show_alert=True)
        logger.info(f'User {callback.from_user.id} remove product id{product_id} from basket')


async def edit_basket_product_from_basket(message: types.Message):
    user_id = message.from_user.id
    if 'add_id' in message.text:
        product_id = int(message.text.replace('/add_id', ''))
        await DB.add_to_basket(product_id=product_id, user_id=user_id)
        logger.info(f'User {message.from_user.id} add product id{product_id} in basket')

    elif 'rem_id' in message.text:
        product_id = int(message.text.replace('/rem_id', ''))
        await DB.remove_from_basket(product_id=product_id, user_id=user_id)
        logger.info(f'User {message.from_user.id} remove product id{product_id} from basket')

    basket = await DB.get_basket(user_id=user_id)
    await message.answer(text=get_basket_msg(basket), reply_markup=get_basket_ikb(basket))


async def clear_basket(callback: types.CallbackQuery):
    asyncio.create_task(DB.clear_basket(user_id=callback.from_user.id))
    await callback.answer(text=f'Все товары удалены из корзины', show_alert=True)
    await callback.message.answer(text=get_basket_msg(basket=None), reply_markup=get_basket_ikb(basket=None))
    logger.info(f'User {callback.from_user.id} cleared all basket')


async def create_order(callback: types.CallbackQuery):
    customer_info = await DB.get_customer_info(user_id=callback.from_user.id)

    if callback.data == 'Оформить заказ':
        # IF CUSTOMER INFO EXISTS THEN CREATE ORDER, ELSE NEED TO WRITE CUSTOMER INFO
        if customer_info:
            await callback.answer(text=f'Проверьте, пожалуйста, ваши данные', show_alert=True)
            await callback.message.answer(text=get_customer_info_msg(customer_info), reply_markup=check_customer_info_ikb)
        else:
            await callback.answer('Перед отправкой заявки необходимо заполнить данные покупателя', show_alert=True)
            await callback.message.answer(text=get_customer_info_msg(customer_info=None), reply_markup=customer_info_ikb)

    elif callback.data == 'Отправить заказ':
        basket = await DB.get_basket(user_id=callback.from_user.id)

        await callback.answer(text=f'Заявка отправлена! Скоро с вами свяжется наш менеджер', show_alert=True)
        logo_img = types.InputFile('database/logo.png')
        await callback.message.answer_photo(photo=logo_img)
        await callback.message.answer(text='🔴 Вы в главном меню бота. Ещё что-то посмотрите?', reply_markup=main_ikb)
        logger.info(f'User {callback.from_user.id} sent order {basket}')

        asyncio.create_task(DB.clear_basket(user_id=callback.from_user.id))

        order_info = {
            'telegram_username': customer_info[2],
            'telegram_name': customer_info[3],
            'name': f'{customer_info[6]} {customer_info[7]}',
            'phone': customer_info[8],
            'address': customer_info[9],
            'order': basket,
        }
        
        OrderEmailNotification(**order_info).send()
        await OrderTelegramNotification(**order_info).send()


def register_basket_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(callback=edit_basket_product_from_products,
                                       text_startswith=['Добавить в корзину', 'Убрать из корзины'])

    dp.register_message_handler(callback=edit_basket_product_from_basket, text_startswith=['/add_id', '/rem_id'])
    dp.register_callback_query_handler(callback=clear_basket, text=['Очистить корзину'])
    dp.register_callback_query_handler(callback=create_order, text=['Оформить заказ', 'Отправить заказ'])
