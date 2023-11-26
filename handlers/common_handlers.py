from aiogram import types, Dispatcher

from loader import dp
from messages import *
from keyboards import *


async def come_back(callback: types.CallbackQuery):
    if callback.data == 'Назад':
        await callback.answer(text='В разработке', show_alert=True)


async def delete_other_messages(message: types.Message):
    await message.delete()


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_other_messages)

    dp.register_callback_query_handler(come_back)
