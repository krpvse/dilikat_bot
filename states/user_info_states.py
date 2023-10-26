from aiogram.dispatcher.filters.state import StatesGroup, State


class UserInfoStatesGroup(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    delivery_address = State()
