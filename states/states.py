from aiogram.dispatcher.filters.state import StatesGroup, State


class CustomerInfoStatesGroup(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    delivery_address = State()


class ProductStatesGroup(StatesGroup):
    category = State()
    product = State()
