from app.exceptions import ClientError, ObjectNotFoundError


class BookBaseError(Exception):
    pass


class BookNotFoundError(BookBaseError, ObjectNotFoundError):
    pass


class BookImportError(BookBaseError, ClientError):
    pass
