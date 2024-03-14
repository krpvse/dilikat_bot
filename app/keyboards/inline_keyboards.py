from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Материалы', callback_data='Материалы'),
            InlineKeyboardButton(text='Оборудование', callback_data='Оборудование')
        ],
        [
            InlineKeyboardButton(text='👨‍🦰', callback_data='Мои данные'),
            InlineKeyboardButton(text='📞', callback_data='Позвонить'),
            InlineKeyboardButton(text='🛒', callback_data='Корзина')
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
            InlineKeyboardButton(text='◀️ Назад', callback_data='Главное меню')
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
            InlineKeyboardButton(text='◀️ Назад', callback_data='Главное меню'),
            InlineKeyboardButton(text='Фрезы', callback_data='Фрезы')
        ]
    ],
    resize_keyboard=True
)

customer_info_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Редактировать', callback_data='Изменить пользователя'),
            InlineKeyboardButton(text='🛒 В корзину', callback_data='Корзина'),
        ],
        [
            InlineKeyboardButton(text='◀️ В главное меню', callback_data='Главное меню'),
        ]
    ],
    resize_keyboard=True
)

check_customer_info_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Редактировать', callback_data='Изменить пользователя'),
            InlineKeyboardButton(text='✅ Всё верно', callback_data='Отправить заказ'),
        ],
        [
            InlineKeyboardButton(text='◀️ В главное меню', callback_data='Главное меню'),
        ]
    ],
    resize_keyboard=True
)

customer_info_change_ikb = InlineKeyboardMarkup(
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
            InlineKeyboardButton(text='◀️ Назад', callback_data='Главное меню')
        ]
    ],
    resize_keyboard=True
)


def get_category_products_ikb(category_type):
    category_products_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='◀️ Назад', callback_data=category_type),  # example of category_type: "Материалы"
            ]
        ],
        resize_keyboard=True
    )
    return category_products_ikb


def get_basket_ikb(basket):
    if basket:
        basket_ikb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Очистить корзину', callback_data='Очистить корзину'),
                    InlineKeyboardButton(text='✅ Оформить', callback_data='Оформить заказ'),
                ],
                [
                    InlineKeyboardButton(text='◀️ Главное меню', callback_data='Главное меню'),
                ]
            ],
            resize_keyboard=True
        )
    else:
        basket_ikb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='◀️ Главное меню', callback_data='Главное меню'),
                ]
            ],
            resize_keyboard=True
        )

    return basket_ikb


def get_product_ikb(category_name, product_id):
    product_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='➕📦', callback_data=f'Добавить в корзину {product_id}'),
                InlineKeyboardButton(text='➖📦', callback_data=f'Убрать из корзины {product_id}')
            ],
            [
                InlineKeyboardButton(text='◀️ Назад', callback_data=category_name),  # example of category_name: "Печи"
                InlineKeyboardButton(text='🛒 В корзину', callback_data='Корзина')
            ]
        ],
        resize_keyboard=True
    )

    return product_ikb
