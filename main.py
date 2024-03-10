import asyncio
import logging
from aiogram import Bot, Dispatcher

from config_reader import config
from database.requests.connect import db_run
from database.requests.triggers import db_get_triggers
from database.requests.actions import db_get_actions
from menu import set_commands
from handlers import main_handlers, answers
from handlers.triggers import add_triggers, show_triggers, remove_triggers
from handlers.actions import add_actions, show_actions, remove_actions
from cash import TRIGGERS, ACTIONS


async def main():
    logging.basicConfig(level=logging.ERROR)
    bot = Bot(token=config.bot_token.get_secret_value())

    dispatcher = Dispatcher()
    dispatcher.include_routers(
        main_handlers.router,
        add_triggers.router, show_triggers.router, remove_triggers.router,
        add_actions.router, show_actions.router, remove_actions.router,
        answers.router,
    )

    await db_run()
    TRIGGERS.extend(await db_get_triggers())
    ACTIONS.extend(await db_get_actions())

    await set_commands(bot)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    # with suppress(TelegramNetworkError):
    asyncio.run(main())
