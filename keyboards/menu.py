from aiogram.types import BotCommand

from loader import bot


async def set_menu():
    bot_commands = [
        BotCommand(command='/start', description='Запустить/перезапустить бот'),
        BotCommand(command='/help', description='Узнать, как пользоваться ботом')
    ]
    await bot.delete_my_commands()
    await bot.set_my_commands(bot_commands)
