from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart

from handlers.additional_functions import temporary_message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Nipaa~!")


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()

    await temporary_message(
        await message.answer(text="Отменено"), message
    )


@router.message(F.new_chat_members)
async def somebody_added(message: Message):
    await message.reply_photo(FSInputFile("media/hello_image.jpg"))
