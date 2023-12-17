from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from app.settings import conf


class HealthView(PydanticView):
    async def get(self) -> r200[web.Response]:
        return web.json_response({'version': conf.SPEC_VERSION})
