import sentry_sdk
from pydantic import HttpUrl
from sentry_sdk.integrations.aiohttp import AioHttpIntegration


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
    ]
    sentry_sdk.init(
        dsn=str(dsn),
        integrations=integrations,
        traces_sample_rate=rate,
        ignore_errors=ignore_errors,
    )
