from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import ActionRemoveState
from database.requests.actions import db_remove_action, db_get_actions
from cash import ACTIONS
from handlers.additional_functions import temporary_message

router = Router()


@router.message(StateFilter(None), Command('action_remove'))
async def remove_action(message: Message, state: FSMContext):
    await state.set_state(ActionRemoveState.choice_remove_action)

    await temporary_message(
        await message.answer(
            'Удалить действие (можно несколько через ";", можно стикер)'
        ), message
    )


@router.message(ActionRemoveState.choice_remove_action, F.text | F.sticker)
async def choosing_remove_action(message: Message, state: FSMContext):
    if message.text:
        for word in message.text.split(';'):
            await db_remove_action(message.chat.id, word.lower().strip())
    elif message.sticker:
        await db_remove_action(message.chat.id, message.sticker.file_unique_id)

    ACTIONS.clear()
    ACTIONS.extend(await db_get_actions())

    await state.clear()

    await temporary_message(
        await message.answer('Удалено'), message
    )
