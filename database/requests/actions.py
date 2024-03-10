from sqlalchemy import select, delete

from database.models import Action
from database.requests.connect import session_begin


@session_begin
async def db_add_action(session, chat_id, interaction, command, text, ):
    stmt = select(Action)\
        .where(Action.chat_id == chat_id)\
        .where(Action.command == command)\
        .where(Action.interaction == interaction)
    action = (await session.scalars(stmt)).all()
    if action:
        await session.delete(action)
    session.add(Action(
        chat_id=chat_id, interaction=interaction, command=command, text=text,
    ))
    await session.commit()
    return True


@session_begin
async def db_get_actions(session):
    stmt = select(Action)
    data = (await session.scalars(stmt)).all()
    await session.commit()

    return [{
        'chat_id': await item.awaitable_attrs.chat_id,
        'interaction': await item.awaitable_attrs.interaction,
        'command': await item.awaitable_attrs.command,
        'text': await item.awaitable_attrs.text,
    } for item in data]


@session_begin
async def db_remove_action(session, chat_id, command):
    stmt = select(Action)\
        .where(Action.chat_id == chat_id)\
        .where(Action.command == command)
    action = (await session.scalars(stmt)).all()
    if action:
        await session.delete(action[0])
    await session.commit()
