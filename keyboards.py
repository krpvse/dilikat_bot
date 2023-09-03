from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Клавиатура для секции главного меню
main_ikb = InlineKeyboardMarkup()
m_ib1 = InlineKeyboardButton(text='Выбрать продукты', callback_data='Категории продуктов')
m_ib2 = InlineKeyboardButton(text='Корзина', callback_data='Корзина')
m_ib3 = InlineKeyboardButton(text='Мои данные', callback_data='Мои данные')
m_ib4 = InlineKeyboardButton(text='Позвонить', callback_data='Позвонить')

main_ikb.add(m_ib1, m_ib2).add(m_ib3, m_ib4)


# Клавиатура для секции категорий продуктов
categories_ikb = InlineKeyboardMarkup()
c_ib1 = InlineKeyboardButton(text='3D принтеры', callback_data='3D принтеры')
c_ib2 = InlineKeyboardButton(text='3D сканеры', callback_data='3D сканеры')
c_ib3 = InlineKeyboardButton(text='Фрезерные станки', callback_data='Фрезерные станки')
c_ib4 = InlineKeyboardButton(text='Печи', callback_data='Печи')
c_ib5 = InlineKeyboardButton(text='Фотополимеры', callback_data='Фотополимеры')
c_ib6 = InlineKeyboardButton(text='CAD CAM блоки', callback_data='CAD CAM блоки')

categories_ikb.add(c_ib1, c_ib2).add(c_ib3, c_ib4).add(c_ib5, c_ib6)


# Клавиатура секции продуктов какой-либо категории
category_products_ikb = InlineKeyboardMarkup()
c_pr_ib1 = InlineKeyboardButton(text='⬅️ Категории', callback_data='Категории продуктов')
c_pr_ib2 = InlineKeyboardButton(text='Главное меню', callback_data='Главное меню')

category_products_ikb .add(c_pr_ib1, c_pr_ib2)


# Клавиатура для секции продукта
product_ikb = InlineKeyboardMarkup()
pr_ib1 = InlineKeyboardButton(text='➕📦', callback_data='Добавить в корзину')
pr_ib2 = InlineKeyboardButton(text='➖📦', callback_data='Убрать из корзины')
pr_ib3 = InlineKeyboardButton(text='Перейти в корзину', callback_data='Корзина')

product_ikb.add(pr_ib1, pr_ib2).add(pr_ib3)


# Клавиатура для c данными пользователя
user_info_ikb = InlineKeyboardMarkup()
ui_ib1 = InlineKeyboardButton(text='⬅️ Главное меню', callback_data='Главное меню')
ui_ib2 = InlineKeyboardButton(text='Изменить данные', callback_data='Изменить данные пользователя')

user_info_ikb.add(ui_ib1, ui_ib2)

