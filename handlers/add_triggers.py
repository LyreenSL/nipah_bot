from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import TriggerAddState
from database.requests import db_add_trigger


router = Router()


@router.message(StateFilter(None), Command('nipah_add'))
async def add_answer(message: Message, state: FSMContext):
    await message.answer('Слово-триггер или слова через ;')
    await state.set_state(TriggerAddState.choice_word)


@router.message(TriggerAddState.choice_word, F.text)
async def choice_word(message: Message, state: FSMContext):
    await state.update_data(choosing_word=message.text.lower())
    await message.answer('Ответ:')
    await state.set_state(TriggerAddState.choice_answer)


@router.message(TriggerAddState.choice_answer, F.text)
async def choice_answer(message: Message, state: FSMContext):
    words = (await state.get_data())["choosing_word"].split(';')
    answer = message.text
    for word in words:
        await db_add_trigger(message.chat.id, word.lower().strip(), answer)
    await message.answer('Добавлено')
    # if await db_add_trigger(message.chat.id, word, answer):
    #     await message.answer(
    #         f'Слово-триггер: {word}\n'
    #         f'Ответ: {answer}'
    #     )
    # else:
    #     await message.answer('Слово уже есть')
    await state.clear()
