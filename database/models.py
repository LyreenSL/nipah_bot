from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Trigger(Base):
    __tablename__ = 'triggers'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    chat_id: Mapped[int]
    word: Mapped[str]
    answer: Mapped[str]


class Action(Base):
    __tablename__ = 'actions'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    chat_id: Mapped[int]
    interaction: Mapped[bool]
    command: Mapped[str]
    text: Mapped[str]
