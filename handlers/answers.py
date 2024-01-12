from aiogram import Router
from aiogram.types import Message

from filters import WordsFilter, DBWordsFilter

router = Router()


@router.message(DBWordsFilter())
async def answer(message: Message, trigger_answer: str):
    await message.answer(trigger_answer)


@router.message(WordsFilter({'типа'}))
async def cmd_tipa(message: Message):
    await message.reply('Тык в ебучку! Говори "нипа"!')


@router.message(WordsFilter({'нипа'}))
async def cmd_nipa(message: Message):
    await message.reply('Nipaa~ погладила тебя по головке')
