from aiogram.types import BotCommand


async def set_commands(bot):
    commands = [
        BotCommand(command='/nipah_start', description='Приветствие'),
        BotCommand(command='/nipah_add', description='Добавить слово-триггер'),
        BotCommand(command='/nipah_remove', description='Удалить слово-триггер'),
        BotCommand(command='/nipah_cancel', description='Прервать действие'),
        BotCommand(command='/nipah_show', description='Показать все слова с ответами'),
        BotCommand(command='/rape', description='c===3'),
        BotCommand(command='/rape_image', description='c===3')
    ]
    await bot.set_my_commands(commands)
