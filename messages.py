from bitrix24 import category_products, product_description
import database as db


product_message = product_description

category_products_message = f'🔴 Выберите продукт\n\n' \
                            f'{category_products}\n\n' \
                            f'<i> Нажмите на id товара для перехода к описанию</i>'


def get_user_info_message(tg_user_id):
    user_info = db.get_user_info(tg_user_id)
    if user_info:
        user_info_message = f'🔴 Информация о вас\n\n' \
                            f'<b>Имя:</b> {user_info[0]} {user_info[1]}\n' \
                            f'<b>Номер телефона:</b> {user_info[2]}\n' \
                            f'<b>Адрес доставки:</b> {user_info[3]}\n\n' \
                            f'<i> Нажмите на id товара для перехода к описанию</i>'
    else:
        user_info_message = '🔴 Мы ещё ничего о вас не знаем!\n' \
                            ' Давайте запишем информацию, чтобы не спрашивать каждый раз?\n\n'
    return user_info_message


