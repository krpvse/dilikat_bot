

bot_info_msg = 'ℹ️ Это бот для заказов от компании Dilikat\n\n'\
                'Здесь вы можете оставить заявку нашим менеджерам, и они оперативно ее обработают\n\n'\
                'Как использовать этот бот?\n'\
                '1. Запустить бот командой /start \n'\
                '2. Добавить интересующие товары в корзину\n'\
                '3. Записать свои контактные данные\n'\
                '4. Проверить, всё ли верно, и отправить заявку!\n\n'


async def get_customer_info_msg(customer_info):
    if customer_info:
        customer_info_msg = f'🔴 Ваши данные\n\n' \
                            f'<b>Имя:</b> {customer_info[6]} {customer_info[7]}\n' \
                            f'<b>Номер телефона:</b> {customer_info[8]}\n' \
                            f'<b>Адрес доставки:</b> {customer_info[9]}'
    else:
        customer_info_msg = '🔴 Мы ничего о вас не знаем!\n\n' \
                            'Запишем информацию, чтобы не спрашивать каждый раз?'
    return customer_info_msg


async def get_basket_msg(basket):
    if basket:
        basket_info_msg = '🔴 У вас в корзине\n\n' \
                           '----------------------------------------------\n\n'
        basket_price = 0
        for product in basket:
            title = product[1]
            product_id = product[0]
            quantity = product[3]
            price = product[2] * quantity

            basket_price += price

            basket_info_msg += f'<b>▪️ </b> {title} /show_id{product_id}\n' \
                                f'<b>- Кол-во:</b> {quantity} шт.\n' \
                                f'<b>- Цена:</b> {price} руб.\n\n' \
                                f'Добавить: /add_id{product_id}  ' \
                                f'Удалить: /rem_id{product_id}\n' \
                                f'----------------------------------------------\n\n'

        basket_info_msg += f'<b>Итого:</b> {basket_price} руб.\n\n'
        basket_info_msg += ('<i>❗️Нажав на кнопку "оформить", вы мгновенно отправите заявку нашему менеджеру. '
                            'Оформляем, или ещё что-то посмотрите?</i>')

    else:
        basket_info_msg = '🔴 Ваша корзина пуста\n\n' \
                            'Посмотрите что-нибудь?'
    return basket_info_msg


async def get_category_products_msg(category_name, products):
    category_products = [product for product in products if category_name in product]

    category_products_msg = '🔴 Какой продукт вас интересует?\n\n'
    for product in category_products:
        id = product[0]
        title = product[1]
        category_products_msg += f'▪️ {title} – /show_id{id}\n\n'

    category_products_msg += '<i><b>Нажимайте на "id" для перехода к описанию</b></i>'
    return category_products_msg


async def get_product_msg(product):
    title = product[1]
    description = product[2]
    price = product[4]
    site_url = product[5]

    product_msg = (f'<b>🔴 {title}\n\n</b>'
                   f'{description}\n\n'
                   f'Цена: {price} руб.\n\n'
                   f'Подробнее на сайте: {site_url}\n\n'
                   f'<i><b>Добавляйте товары в корзину, затем переходите к заказу</b></i>')

    return product_msg
