from aiohttp import web

from app.library.views import BookImportView, BooksView, BookView


def setup_routes(app: web.Application) -> None:
    app.router.add_view('/books', BooksView, name='books')
    app.router.add_post('/books/import', BookImportView, name='books_import')
    app.router.add_view('/books/{uid}', BookView, name='book')
