from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from config_reader import config

router = Router()


def get_mention(message):
    return f'[{message.from_user.full_name}](tg://user?id={message.from_user.id})'


@router.message(F.new_chat_members)
async def somebody_added(message: Message):
    await message.reply_photo(FSInputFile("media/hello_image.jpg"))


@router.message((F.text == '/rape') | (F.sticker.file_unique_id == 'AgADaEIAAknnuEg'))
async def cmd_rape(message: Message):

    dom = get_mention(message)
    if message.reply_to_message:
        sub = get_mention(message.reply_to_message)
        if message.reply_to_message.from_user.id == int(config.bot_token.get_secret_value()[:10]):
            sub, dom = dom, sub
    else:
        sub = 'воздух'

    if sub == dom:
        answ = f'{dom} хорошенько подрочил(а) себе анус'
    else:
        answ = f'{dom} жёстко выебал(а) {sub}'

    await message.answer(text=answ, parse_mode='Markdown')


@router.message(Command(commands=["rape_image"]))
async def cmd_rape(message: Message):

    dom = get_mention(message)
    if message.reply_to_message:
        answ = f'{dom} жёстко выебал(а) персонажа на картинке'
    else:
        answ = f'{dom} жёстко выебал(а) воздух'

    await message.answer(text=answ, parse_mode='Markdown')


@router.message(F.text.lower().startswith('помолиться'))
async def cmd_prey(message: Message):
    user = get_mention(message)
    god = message.text[10:]
    await message.answer(f'{user} помолил(а)ся{god}', parse_mode='Markdown')
