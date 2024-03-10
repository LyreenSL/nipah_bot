from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from cash import ACTIONS
from handlers.additional_functions import temporary_message

router = Router()


@router.message(Command(commands=["action_show"]))
async def show_actions(message: Message):
    output = ''.join(
        f"\n{item['command']} {' (взаимодействие)' if item['interaction'] else ''}\n"
        for item in ACTIONS if item['chat_id'] == message.chat.id
    )
    await temporary_message(
        await message.answer(f'Список команд:\n{output}'), message
    )

