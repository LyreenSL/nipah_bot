from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['nipah_start', 'start']))
async def cmd_start(message: Message):
    await message.answer("Nipaa~!")


@router.message(Command(commands=["nipah_cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Отменено")
