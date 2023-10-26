from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Материалы', callback_data='Материалы'),
            InlineKeyboardButton(text='Оборудование', callback_data='Оборудование')
        ],
        [
            InlineKeyboardButton(text='Мои данные', callback_data='Мои данные'),
            InlineKeyboardButton(text='Позвонить', callback_data='Позвонить')
        ]
    ],
    resize_keyboard=True
)


equipment_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='3D принтеры', callback_data='3D принтеры'),
            InlineKeyboardButton(text='3D сканеры', callback_data='3D сканеры')
        ],
        [
            InlineKeyboardButton(text='Фрезерные станки', callback_data='Фрезерные станки'),
            InlineKeyboardButton(text='Печи', callback_data='Печи')
        ],
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад')
        ]
    ],
    resize_keyboard=True
)


materials_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Фотополимеры', callback_data='Фотополимеры'),
            InlineKeyboardButton(text='CAD CAM блоки', callback_data='CAD CAM блоки')
        ],
        [
            InlineKeyboardButton(text='Фрезы', callback_data='Фрезы'),
            InlineKeyboardButton(text='Перейти в корзину', callback_data='Корзина')
        ],
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад')
        ]
    ],
    resize_keyboard=True
)


product_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='➕📦', callback_data='Добавить в корзину'),
            InlineKeyboardButton(text='➖📦', callback_data='Убрать из корзины')
        ],
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад')
        ]
    ],
    resize_keyboard=True
)


user_info_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад'),
            InlineKeyboardButton(text='Редактировать', callback_data='Изменить пользователя')
        ]
    ],
    resize_keyboard=True
)


user_info_change_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Не изменять пользователя')
        ]
    ],
    resize_keyboard=True
)


call_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад')
        ]
    ],
    resize_keyboard=True
)


basket_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад'),
            InlineKeyboardButton(text='Оформить', callback_data='Оформить заказ')
        ]
    ],
    resize_keyboard=True
)


category_products_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='Назад'),
            InlineKeyboardButton(text='Главное меню', callback_data='Главное меню')
        ]
    ],
    resize_keyboard=True
)
