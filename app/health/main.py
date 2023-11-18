from aiohttp import web

from app.health.routes import setup_routes


def init_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    return app
