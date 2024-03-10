from sqlalchemy import select, delete

from database.models import Trigger
from database.requests.connect import session_begin


@session_begin
async def db_add_trigger(session, chat_id, word, answer):
    stmt = select(Trigger)\
        .where(Trigger.chat_id == chat_id)\
        .where(Trigger.word == word)
    trigger_pair = (await session.scalars(stmt)).all()
    if trigger_pair:
        await session.delete(trigger_pair[0])
    session.add(Trigger(chat_id=chat_id, word=word, answer=answer))
    await session.commit()
    return True


@session_begin
async def db_get_triggers(session):
    # stmt = select(Trigger).where(Trigger.chat_id == chat_id)
    # triggers_pairs = (await session.scalars(stmt)).all()
    # await session.commit()
    # return [
    #     (
    #         await pair.awaitable_attrs.word,
    #         await pair.awaitable_attrs.answer
    #     ) for pair in triggers_pairs
    # ]
    stmt = select(Trigger)
    data = (await session.scalars(stmt)).all()
    await session.commit()

    return [{
        'chat_id': await item.awaitable_attrs.chat_id,
        'word': await item.awaitable_attrs.word,
        'answer': await item.awaitable_attrs.answer,
    } for item in data]


@session_begin
async def db_remove_trigger(session, chat_id, word):
    stmt = select(Trigger)\
        .where(Trigger.chat_id == chat_id)\
        .where(Trigger.word == word)
    trigger_pair = (await session.scalars(stmt)).all()
    if trigger_pair:
        await session.delete(trigger_pair[0])
        # await session.commit()
        # return True
    await session.commit()
    # return False
