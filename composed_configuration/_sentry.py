from typing import Type

from configurations import values

from ._base import ComposedConfiguration, ConfigMixin


class SentryMixin(ConfigMixin):
    """
    Configure Sentry.io error reporting.

    This requires the `sentry-sdk` package to be installed.

    The `DJANGO_SENTRY_DSN` environment variable should be externally set to a Sentry DSN.

    The `DJANGO_SENTRY_ENVIRONMENT` and `DJANGO_SENTRY_RELEASE` environment variables may also
    be set, if desired.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += [
            'composed_configuration.sentry.apps.SentryConfig',
        ]

    SENTRY_DSN = values.Value(None)

    SENTRY_ENVIRONMENT = values.Value(None)

    SENTRY_RELEASE = values.Value(None)
