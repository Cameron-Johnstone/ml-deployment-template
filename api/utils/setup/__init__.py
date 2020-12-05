import os

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .middlewares import ApiTokenMiddleware, TimingMiddleware


def _setup_sentry():
    sentry_dsn = os.getenv("SENTRY_DSN")

    sentry_environment = os.getenv("SENTRY_ENVIRONMENT")
    if sentry_environment is None:
        sentry_environment = "unknown"

    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=sentry_environment
    )


def _add_middlewares(app: FastAPI) -> None:
    app.add_middleware(ApiTokenMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(SentryAsgiMiddleware)


def setup(app: FastAPI) -> None:
    _setup_sentry()
    _add_middlewares(app)
