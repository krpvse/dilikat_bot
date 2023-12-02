from loader import db, catalog


hello_msg = '👋 Привет! Это бот для заказов Dilikat\nЗдесь вы можете оставить заявку, ' \
                'а наши менеджеры оперативно её обработают.\n\n🔴 Что вас интересует?'

main_section_msg = '🔴 Вы в главном меню бота. Хотите сделать заказ?'

materials_section_msg = '🔴 Какие расходные материалы интересуют?'

equipment_section_msg = '🔴 Какое оборудование интересует?'

call_section_msg = '🔴 Наш номер: 88003018733\nНабирайте скорей, мы ждем 😉'



def get_customer_info_msg(tg_user_id):
    customer_info = db.get_customer_info(tg_user_id)
    if customer_info:
        customer_info_msg = f'🔴 Ваши данные\n\n' \
                            f'<b>Имя:</b> {customer_info[0]} {customer_info[1]}\n' \
                            f'<b>Номер телефона:</b> {customer_info[2]}\n' \
                            f'<b>Адрес доставки:</b> {customer_info[3]}'
    else:
        customer_info_msg = '🔴 Мы ничего о вас не знаем!\n\n' \
                            'Запишем информацию, чтобы не спрашивать каждый раз?'
    return customer_info_msg



def get_basket_info_msg(tg_user_id):
    basket_info = db.get_customer_basket(tg_user_id)

    if basket_info:
        basket_info_msg = '🔴 Ваша корзина\n\n'
        for product in basket_info:
            basket_info_msg += f'<b>▪️ </b> {product[0]}\n' \
                                f'<b>Кол-во:</b> {product[1]}\n' \
                                f'<b>Цена:</b> СТОИМОСТЬ\n\n'

        basket_info_msg += f'<b>Итого в сумме:</b> СТОИМОСТЬ\n\n'
        basket_info_msg += 'Оформляем, или ещё что-то посмотрите?'

    else:
        basket_info_msg = '🔴 Ваша корзина пуста\n\n' \
                            'Выберете что-нибудь?'
    return basket_info_msg



change_first_name_msg = f'🔴 Ваше имя?\n\n' \
                        f'<i>Напишите в одном сообщении, пожалуйста</i>'

change_last_name_msg = f'🔴 Ваша фамилия?\n\n' \
                       f'<i>Напишите в одном сообщении, пожалуйста</i>'

change_phone_number_msg = f'🔴 Номер телефона?\n\n' \
                          f'<i>Напишите в одном сообщении, пожалуйста</i>'

change_delivery_address_msg = f'🔴 Ваш адрес для доставки?\n\n' \
                              f'<i>Напишите в одном сообщении, пожалуйста</i>'



def get_category_products_msg(category_name):
    category_products = [product for product in catalog if category_name in product]

    category_products_msg = '🔴 Какой продукт вас интересует?\n\n'

    for product in category_products:
        id = product[0]
        title = product[1]
        category_products_msg += f'▪️ {title} – /id{id}\n\n'

    category_products_msg += '<i><b>Нажимайте на "id" для перехода к описанию</b></i>'
    return category_products_msg



def get_product_msg(product_id):
    product = [product for product in catalog if product_id in product][0]

    title = product[1]
    description = product[2]
    price = product[4]
    site_url = product[5]

    product_msg = (f'<b>🔴 {title}\n\n</b>'
                   f'{description}\n\n'
                   f'Цена: {price} руб.\n\n'
                   f'Подробнее на сайте: {site_url}')

    return product_msg
