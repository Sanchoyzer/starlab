from datetime import date, datetime
from enum import StrEnum, unique
from uuid import UUID, uuid4

from sqlalchemy import Enum, MetaData, func, sql
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@unique
class GenreType(StrEnum):
    NOVEL = 'Novel'
    DETECTIVE = 'Detective'
    FANTASY = 'Fantasy'
    SCIENCE_FICTION = 'Science Fiction'
    HORROR = 'Horror'
    ADVENTURE = 'Adventure'
    POPULAR_SCIENCE = 'Popular Science'
    RELIGIOUS_LITERATURE = 'Religious Literature'
    NON_FICTION = 'Non-fiction'
    POETRY = 'Poetry'


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s_%(column_1_name)s_%(column_2_name)s',
            'ck': 'ck_%(table_name)s_`%(constraint_name)s`',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s',
        },
    )


class BaseEntity(Base):
    __abstract__ = True

    uid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Book(BaseEntity):
    __tablename__ = 'book'
    __table_args__ = {'schema': 'library'}  # noqa: RUF012

    name: Mapped[str] = mapped_column(index=True)
    author: Mapped[str] = mapped_column(index=True)
    published_at: Mapped[date]
    genre: Mapped[GenreType] = mapped_column(
        Enum(*list(GenreType._value2member_map_.keys()), name='book_genre_enum', schema='library'),
        index=True,
    )
    url: Mapped[str]
    available_for_view: Mapped[bool] = mapped_column(server_default=sql.true())
    available_for_download: Mapped[bool] = mapped_column(server_default=sql.true())
