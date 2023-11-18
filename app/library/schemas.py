from typing import Annotated, ClassVar
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    NonNegativeInt,
    PastDate,
    PastDatetime,
    PositiveInt,
    field_validator,
)

from app.library.models import GenreType


class Model(BaseModel, validate_assignment=True):
    model_config: ClassVar = ConfigDict(extra='forbid', frozen=True)


class BookCreateRequest(Model):
    name: Annotated[str, Field(min_length=1, max_length=256)]
    author: Annotated[str, Field(min_length=1, max_length=256)]
    published_at: Annotated[PastDate, Field(...)]
    genre: Annotated[GenreType, Field(min_length=1)]
    url: Annotated[str, Field(...)]

    @field_validator('url')
    @classmethod
    def check_correct_url(cls: type['BookCreateRequest'], v: str) -> str:
        HttpUrl(v)
        return v


class BookCreateResponse(BookCreateRequest):
    model_config: ClassVar = ConfigDict(from_attributes=True)

    uid: Annotated[UUID, Field()]
    created_at: Annotated[PastDatetime, Field()]
    available_for_view: Annotated[bool, Field()]
    available_for_download: Annotated[bool, Field()]


class BookListFilters(Model):
    name: Annotated[str | None, Field()] = None
    author: Annotated[str | None, Field()] = None
    published_at: Annotated[PastDate | None, Field()] = None
    genre: Annotated[list[GenreType] | None, Field()] = None
    offset: Annotated[NonNegativeInt, Field()]
    limit: Annotated[PositiveInt, Field()]


class BookItemResponse(BookCreateResponse):
    pass


class BookListResponse(Model):
    items: list[BookItemResponse]
