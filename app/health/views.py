from aiohttp import web

from app.settings import conf


async def handle_health(request: web.Request) -> web.Response:  # noqa: ARG001
    return web.json_response({'version': conf.SPEC_VERSION})
