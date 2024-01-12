from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import TriggerRemoveState
from database.requests import db_remove_trigger

router = Router()


@router.message(StateFilter(None), Command('nipah_remove'))
async def remove_answer(message: Message, state: FSMContext):
    await message.answer('Удалить слово-триггер:')
    await state.set_state(TriggerRemoveState.choice_remove_word)


@router.message(TriggerRemoveState.choice_remove_word, F.text)
async def choosing_remove_answer(message: Message, state: FSMContext):
    if await db_remove_trigger(message.chat.id, message.text.lower()):
        await message.answer('Удалено')
    else:
        await message.answer('Слово не найдено')
    await state.clear()
