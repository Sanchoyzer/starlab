from aiohttp import web

from app.health.views import HealthView


def setup_routes(app: web.Application) -> None:
    app.router.add_get('/', HealthView, name='health', allow_head=False)
