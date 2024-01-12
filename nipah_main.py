import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from contextlib import suppress

from config_reader import config
from database.requests import db_run
from menu import set_commands
from handlers import main_handlers, answers, \
    add_triggers, show_triggers, remove_triggers, other_handlers


async def main():
    logging.basicConfig(level=logging.ERROR)
    bot = Bot(token=config.bot_token.get_secret_value())
    dispatcher = Dispatcher()
    dispatcher.include_routers(
        main_handlers.router, add_triggers.router, show_triggers.router,
        remove_triggers.router, answers.router, other_handlers.router
    )
    await db_run()
    await set_commands(bot)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    with suppress(TelegramNetworkError):
        asyncio.run(main())
