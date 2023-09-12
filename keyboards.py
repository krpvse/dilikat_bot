from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Keyboard buttons
main_btn = InlineKeyboardButton(text='Главное меню', callback_data='Главное меню')
back_btn = InlineKeyboardButton(text='◀️ Назад', callback_data='Назад')

materials_btn = InlineKeyboardButton(text='Материалы', callback_data='Материалы')
equipment_btn = InlineKeyboardButton(text='Оборудование', callback_data='Оборудование')
user_info_btn = InlineKeyboardButton(text='Мои данные', callback_data='Мои данные')
call_btn = InlineKeyboardButton(text='Позвонить', callback_data='Позвонить')

product1_btn = InlineKeyboardButton(text='3D принтеры', callback_data='3D принтеры')
product2_btn = InlineKeyboardButton(text='3D сканеры', callback_data='3D сканеры')
product3_btn = InlineKeyboardButton(text='Фрезерные станки', callback_data='Фрезерные станки')
product4_btn = InlineKeyboardButton(text='Печи', callback_data='Печи')
material1_btn = InlineKeyboardButton(text='Фотополимеры', callback_data='Фотополимеры')
material2_btn = InlineKeyboardButton(text='CAD CAM блоки', callback_data='CAD CAM блоки')
material3_btn = InlineKeyboardButton(text='Фрезы', callback_data='Фрезы')

show_basket_btn = InlineKeyboardButton(text='Перейти в корзину', callback_data='Корзина')
add_basket_product_btn = InlineKeyboardButton(text='➕📦', callback_data='Добавить в корзину')
remove_basket_product_btn = InlineKeyboardButton(text='➖📦', callback_data='Убрать из корзины')
order_btn = InlineKeyboardButton(text='Оформить', callback_data='Оформить заказ')

change_user_info_btn = InlineKeyboardButton(text='Редактировать', callback_data='Изменить данные пользователя')


# Main keyboard
main_ikb = InlineKeyboardMarkup(inline_keyboard=[[materials_btn, equipment_btn], [user_info_btn, call_btn]])

# Equipment keyboard
equipment_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [product1_btn, product2_btn],
    [product3_btn, product4_btn],
    [back_btn]
])

# Materials keyboard
materials_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [material1_btn, material2_btn],
    [back_btn, material3_btn]
])

# Product keyboard
product_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [add_basket_product_btn, remove_basket_product_btn],
    [back_btn]
])

# User info keyboard
user_info_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [back_btn, change_user_info_btn]
])

# Call keyboard
call_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [back_btn]
])

# Basket keyboard
basket_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [back_btn, order_btn]
])

# Category produсts keyboard
category_products_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [back_btn, main_btn]
])
