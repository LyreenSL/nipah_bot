from asyncio import sleep


def get_mention(message):
    return f'[{message.from_user.full_name}](tg://user?id={message.from_user.id})'


async def temporary_message(answer, message=None):
    await sleep(666)

    try:
        await answer.delete()
    except Exception as e:
        pass

    try:
        await message.delete()
    except Exception as e:
        pass
