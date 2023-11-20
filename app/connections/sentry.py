import sentry_sdk
from pydantic import HttpUrl
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.asyncpg import AsyncPGIntegration


def setup_sentry(
    dsn: HttpUrl | None,
    rate: float = 1.0,
    ignore_errors: list[type | str] | None = None,
) -> None:
    if not dsn:
        return
    ignore_errors = ignore_errors or []
    integrations = [
        AioHttpIntegration(),
        AsyncioIntegration(),
        AsyncPGIntegration(),
    ]
    sentry_sdk.init(
        dsn=str(dsn),
        integrations=integrations,
        traces_sample_rate=rate,
        ignore_errors=ignore_errors,
    )
