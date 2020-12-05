import sentry_sdk
from api.utils.setup.config import SENTRY_DSN, SENTRY_ENVIRONMENT


def setup_sentry():
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT
    )
