from collections.abc import Callable

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError, HTTPNotFound
from aiohttp_pydantic import oas

from app.connections.sentry import setup_sentry
from app.exceptions import ClientError, ObjectNotFoundError, ServerError
from app.health.main import init_app as init_health_app
from app.library.main import init_app as init_library_app
from app.settings import conf


@web.middleware
async def error_middleware(request: web.Request, handler: Callable) -> web.Response:
    try:
        return await handler(request)
    except ObjectNotFoundError as exc:
        return web.json_response({'error': str(exc)}, status=HTTPNotFound.status_code)
    except ClientError as exc:
        return web.json_response({'error': str(exc)}, status=HTTPBadRequest.status_code)
    except ServerError as exc:
        return web.json_response({'error': str(exc)}, status=HTTPInternalServerError.status_code)


async def init_app() -> web.Application:
    setup_sentry(dsn=conf.SENTRY_DSN)

    app = web.Application(middlewares=[error_middleware])
    app.add_subapp('/v1/library', library_app := init_library_app())
    app['library_app'] = library_app
    app.add_subapp('/health', health_app := init_health_app())
    app['health_app'] = health_app

    oas.setup(
        app=app,
        url_prefix=conf.SPEC_URL_PREFIX,
        version_spec=conf.SPEC_VERSION,
        title_spec=conf.SPEC_TITLE,
    )
    return app
