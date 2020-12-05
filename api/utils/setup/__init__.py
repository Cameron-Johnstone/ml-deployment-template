from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .middlewares import ApiTokenMiddleware, TimingMiddleware
from .sentry import setup_sentry


def setup(app: FastAPI) -> None:
    # Custom Middlewares
    app.add_middleware(ApiTokenMiddleware)
    app.add_middleware(TimingMiddleware)
    
    # Sentry    
    setup_sentry()
    app.add_middleware(SentryAsgiMiddleware)
