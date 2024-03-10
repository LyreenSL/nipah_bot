from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import TriggerAddState
from database.requests.triggers import db_add_trigger
from cash import TRIGGERS
from handlers.additional_functions import temporary_message

router = Router()


@router.message(StateFilter(None), Command('trigger_add'))
async def add_answer(message: Message, state: FSMContext):
    await state.set_state(TriggerAddState.choice_word)

    await temporary_message(
        await message.answer(
            'Введите слово-триггер или слова через ";"'
        ), message
    )


@router.message(TriggerAddState.choice_word, F.text)
async def choice_word(message: Message, state: FSMContext):
    await state.update_data(word=message.text.lower())
    await state.set_state(TriggerAddState.choice_answer)

    await temporary_message(
        await message.answer('Введите ответ:'), message
    )


@router.message(TriggerAddState.choice_answer, F.text)
async def choice_answer(message: Message, state: FSMContext):
    words = (await state.get_data())['word'].split(';')

    for word in words:
        await db_add_trigger(
            chat_id=message.chat.id,
            word=word.lower().strip(),
            answer=message.text,
        )
        TRIGGERS.append({
            'chat_id': message.chat.id,
            'word': word.lower().strip(),
            'answer': message.text
        })

    await state.clear()

    await temporary_message(
        await message.answer('Добавлено'), message
    )
