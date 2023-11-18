class ClientError(Exception):
    pass


class ServerError(Exception):
    pass


class ObjectNotFoundError(ClientError):
    pass
