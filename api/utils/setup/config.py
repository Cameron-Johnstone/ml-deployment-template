import os


# Sentry 
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT")

# API Token
API_KEY: str = os.getenv("API_TOKEN")