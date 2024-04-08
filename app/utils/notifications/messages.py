

def create_telegram_order_msgs(order, customer):
    msg1 = (f'<b>🎉 У вас новый заказ!</b>\n\n'
            f'Логин в Telegram: {customer[2]}\n'
            f'Имя в Telegram: {customer[3]}\n'
            f'Имя: {customer[6]} {customer[7]}\n'
            f'Телефон: {customer[8]}\n'
            f'Адрес: {customer[9]}')

    msg2 = f'Данные заказа ({customer[6]} {customer[7]}):\n\n'
    for product in order:
        msg2 += (f'Товар: {product[1]}\n'
                 f'Цена: {product[2]} руб.\n'
                 f'Количество: {product[3]} шт.\n\n')

    return msg1, msg2


def create_email_order_msg(order, customer):
    subject = f'Новый заказ от {customer[6]} {customer[7]} / Telegram-бот'

    text = (f'Новый заказ из Telegram-бота!\n\n'
            f'Логин в Telegram: {customer[2]}\n'
            f'Имя в Telegram: {customer[3]}\n'
            f'Имя: {customer[6]} {customer[7]}\n'
            f'Телефон: {customer[8]}\n'
            f'Адрес: {customer[9]}')

    text += f'\n\nДанные заказа:\n'
    for product in order:
        text += (f'Товар: {product[1]}\n'
                 f'Цена: {product[2]} руб.\n'
                 f'Количество: {product[3]} шт.\n\n')

    return subject, text
