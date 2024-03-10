from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import ActionAddState
from database.requests.actions import db_add_action
from cash import ACTIONS
from handlers.additional_functions import temporary_message

router = Router()


@router.message(StateFilter(None), Command('action_add'))
async def add_action(message: Message, state: FSMContext):
    await state.set_state(ActionAddState.choice_interaction)

    await temporary_message(
        await message.answer(
            'Является ли команда взаимодействием? '
            '(Пишется ли в конце имя пользователя, '
            'на сообщение которого ответили командой?) (да / нет)'
        ), message
    )


@router.message(ActionAddState.choice_interaction, F.text)
async def chose_interaction(message: Message, state: FSMContext):
    answ = message.text.lower()

    if answ not in {'да', 'нет'}:
        await temporary_message(
            await message.answer(
                'Недопустимое значение (да или нет?)'
            ), message
        )
        return

    await state.update_data(
        interaction=True if answ == 'да' else False
    )
    await state.set_state(ActionAddState.choice_command)

    await temporary_message(
        await message.answer(
            'Введите команду или несколько, разделяя ";" (можно стикер)'
        ), message
    )


@router.message(ActionAddState.choice_command, F.text | F.sticker)
async def choice_command(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(command=message.text.lower())

    elif message.sticker:
        await state.update_data(command=message.sticker.file_unique_id)

    else:
        await state.clear()

        await temporary_message(
            await message.answer(
                'Что-то пошло не так, операция отменена'
            ), message
        )
        return

    await state.set_state(ActionAddState.choice_text)

    await temporary_message(
        await message.answer(
            'Введите текст команды (желательно с маленькой буквы, '
            'так как предложение будет начинаться с юзернейма)'
        ), message
    )


@router.message(ActionAddState.choice_text, F.text)
async def choice_answer(message: Message, state: FSMContext):
    commands = (await state.get_data())['command'].split(';')
    interaction = (await state.get_data())['interaction']

    for command in commands:
        await db_add_action(
            chat_id=message.chat.id,
            interaction=interaction,
            command=command,
            text=message.text,
        )
        ACTIONS.append({
            'chat_id': message.chat.id,
            'interaction': interaction,
            'command': command,
            'text': message.text,
        })

    await state.clear()

    await temporary_message(
        await message.answer('Добавлено'), message
    )
