import io
from datetime import date
from uuid import UUID

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest, HTTPCreated, HTTPOk
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r201, r404
from pydantic import Field

from app.library.exceptions import BookImportError, BookNotFoundError
from app.library.schemas import (
    BookCreateRequest,
    BookCreateResponse,
    BookItemResponse,
    BookListFilters,
    BookListResponse,
    GenreType,
    Model,
)
from app.library.services import BookService


class BaseView(PydanticView):
    @staticmethod
    def _json_response(obj: Model, status_code: int = HTTPOk.status_code) -> web.Response:
        return web.json_response(obj.model_dump_json(), status=status_code, dumps=lambda x: x)


class BooksView(BaseView):
    service = BookService

    async def post(self, book_in: BookCreateRequest) -> r201[BookCreateResponse]:
        book = await self.service.create(book_in=book_in)
        book_out = BookCreateResponse.model_validate(book)
        return self._json_response(book_out, status_code=HTTPCreated.status_code)

    async def get(  # noqa: PLR0913
        self,
        name: str | None = None,
        author: str | None = None,
        published_at: date | None = None,
        genre: list[GenreType] = Field(default_factory=list),  # noqa: B008
        offset: int = 0,
        limit: int = 10,
    ) -> r200[BookListResponse]:
        filters = BookListFilters.model_validate(
            {
                'name': name,
                'author': author,
                'published_at': published_at,
                'genre': genre,
                'offset': offset,
                'limit': limit,
            },
        )
        books = await self.service.get_list(filters=filters)
        books_out = BookListResponse.model_validate({'items': books})
        return self._json_response(books_out)


class BookView(BaseView):
    service = BookService

    async def get(self, uid: UUID, /) -> r200[BookItemResponse] | r404:
        if not (book := await self.service.get_one(uid=uid)):
            raise BookNotFoundError(f'book {uid=} not found')
        book_out = BookItemResponse.model_validate(book)
        return self._json_response(book_out)


class BookImportView(BaseView):
    service = BookService

    async def post(self) -> web.Response:
        try:
            reader = await self.request.multipart()
        except Exception as exc:  # noqa: BLE001
            raise BookImportError(repr(exc)) from exc
        while True:
            if (part_item := await reader.next()) is None:
                break
            if part_item.name == 'file' and part_item.filename:
                data = await part_item.read()
                await self.service.import_books(data=io.BytesIO(data))
                return web.Response()
        return web.Response(status=HTTPBadRequest.status_code, text='Expected an Excel file')
