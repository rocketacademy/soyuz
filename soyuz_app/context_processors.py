from django.conf import settings
from django.http import HttpRequest


def frontend_keys(request: HttpRequest):
    sentry_dsn = settings.SENTRY_DSN if getattr(settings, "SENTRY_DSN", False) else ""
    ga_key = (
        settings.GOOGLE_ANALYTICS_KEY
        if getattr(settings, "GOOGLE_ANALYTICS_KEY", False)
        else ""
    )

    return {
        "SENTRY_DSN": sentry_dsn,
        "GA_KEY": ga_key,
    }
