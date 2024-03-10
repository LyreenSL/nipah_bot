from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from cash import TRIGGERS
from handlers.additional_functions import temporary_message

router = Router()


@router.message(Command(commands=["trigger_show"]))
async def show_triggers(message: Message):
    # triggers_pairs = await db_get_triggers(message.chat.id)
    # output = ''.join(f'\n{pair[0]}: {pair[1]}\n' for pair in triggers_pairs)
    output = ''.join(
        f"\n{item['word']}: {item['answer']}\n" for item in TRIGGERS
        if item['chat_id'] == message.chat.id
    )

    await temporary_message(
        await message.answer(f'Слова-триггеры с ответами:\n{output}'), message
    )
