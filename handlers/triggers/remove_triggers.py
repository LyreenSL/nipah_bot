from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import TriggerRemoveState
from database.requests.triggers import db_remove_trigger, db_get_triggers
from cash import TRIGGERS
from handlers.additional_functions import temporary_message

router = Router()


@router.message(StateFilter(None), Command('trigger_remove'))
async def remove_trigger(message: Message, state: FSMContext):
    await state.set_state(TriggerRemoveState.choice_remove_word)

    await temporary_message(
        await message.answer(
            'Удалить слово-триггер (можно несколько через ";")'
        ), message
    )


@router.message(TriggerRemoveState.choice_remove_word, F.text)
async def choosing_remove_trigger(message: Message, state: FSMContext):
    for word in message.text.split(';'):
        await db_remove_trigger(message.chat.id, word.lower().strip())
        TRIGGERS.clear()
        TRIGGERS.extend(await db_get_triggers())

    await state.clear()

    await temporary_message(
        await message.answer('Удалено'), message
    )

    # if await db_remove_trigger(message.chat.id, message.text.lower()):
    #     await message.answer('Удалено')
    #     TRIGGERS.clear()
    #     TRIGGERS.extend(await db_get_triggers())
    # else:
    #     await message.answer('Слово не найдено')
