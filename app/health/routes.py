from aiohttp import web

from app.health.views import handle_health


def setup_routes(app: web.Application) -> None:
    app.router.add_get('/', handle_health, name='health')
