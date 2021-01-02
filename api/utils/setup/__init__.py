from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .middlewares import ApiTokenMiddleware, TimingMiddleware
from .sentry import setup_sentry
from .download_sentence_transformer import get_sentence_transformer


def setup_api(app: FastAPI) -> None:
    # Custom Middlewares
    app.add_middleware(ApiTokenMiddleware)
    app.add_middleware(TimingMiddleware)
    
    # Sentry    
    setup_sentry()
    app.add_middleware(SentryAsgiMiddleware)


def setup_resources():
    sentence_transformer = get_sentence_transformer()
    
    return (sentence_transformer)
