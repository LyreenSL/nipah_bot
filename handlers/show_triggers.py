from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.requests import db_get_triggers

router = Router()


@router.message(Command(commands=["nipah_show"]))
async def show(message: Message):
    triggers_pairs = await db_get_triggers(message.chat.id)
    output = ''.join(f'\n{pair[0]}: {pair[1]}\n' for pair in triggers_pairs)
    await message.answer(f'Слова-триггеры с ответами:\n{output}')
