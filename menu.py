from aiogram.types import BotCommand


async def set_commands(bot):
    commands = [
        BotCommand(command='/start', description='Приветствие'),
        BotCommand(command='/cancel', description='Прервать действие'),
        BotCommand(command='/trigger_add', description='Добавить слово-триггер'),
        BotCommand(command='/trigger_remove', description='Удалить слово-триггер'),
        BotCommand(command='/trigger_show', description='Показать все слова с ответами'),
        BotCommand(command='/action_add', description='Добавить действие'),
        BotCommand(command='/action_remove', description='Удалить действие'),
        BotCommand(command='/action_show', description='Показать все действия'),
        # BotCommand(command='/rape', description='c===3'),
        # BotCommand(command='/rape_image', description='c===3'),
    ]
    await bot.set_my_commands(commands)
