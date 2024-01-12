from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models import Base, Trigger
from config_reader import config

engine = create_async_engine(config.db_address)
async_session = async_sessionmaker(engine, expire_on_commit=False)


def session_begin(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            async with session.begin():
                return await func(session, *args, **kwargs)
    return wrapper


async def db_run():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


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
async def db_get_triggers(session, chat_id):
    stmt = select(Trigger).where(Trigger.chat_id == chat_id)
    triggers_pairs = (await session.scalars(stmt)).all()
    await session.commit()
    return [
        (
            await pair.awaitable_attrs.word,
            await pair.awaitable_attrs.answer
        ) for pair in triggers_pairs
    ]


@session_begin
async def db_remove_trigger(session, chat_id, word):
    stmt = select(Trigger)\
        .where(Trigger.chat_id == chat_id)\
        .where(Trigger.word == word)
    trigger_pair = (await session.scalars(stmt)).all()
    if trigger_pair:
        await session.delete(trigger_pair[0])
        await session.commit()
        return True
    await session.commit()
    return False
