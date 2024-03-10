from aiogram import Router
from aiogram.types import Message

from filters import WordsFilter, DBWordsFilter, DBActionsFilter
from handlers.additional_functions import get_mention

router = Router()


@router.message(DBActionsFilter())
async def answer(
        message: Message,
        action_text: str,
        action_interaction: bool,
        action_add_text: str,
):
    if not message.reply_to_message and action_interaction:
        return
    answ = (f'{get_mention(message)} '
            f'{action_text} '
            f'{get_mention(message.reply_to_message) if action_interaction else ""}'
            f'{action_add_text}')
    await message.reply(text=answ, parse_mode='Markdown')


@router.message(DBWordsFilter())
async def answer(message: Message, trigger_answer: str):
    await message.reply(trigger_answer)


@router.message(WordsFilter({'типа'}))
async def tipa(message: Message):
    await message.reply('Тык в ебучку! Говори "нипа"!')


@router.message(WordsFilter({'нипа'}))
async def nipa(message: Message):
    await message.reply('Nipaa~ погладила тебя по головке')
