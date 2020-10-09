import logging
from typing import Type

from configurations import values

from ._base import ComposedConfiguration, ConfigMixin


class SentryConfig(ConfigMixin):
    """
    Configure Sentry.io error reporting.

    This requires the `sentry-sdk` package to be installed.

    The `SENTRY_DSN` environment variable should be externally set to a Sentry DSN.
    """

    # Sentry documents this and other environment variables (SENTRY_RELEASE, etc.) to have no
    # DJANGO_ prefix, so follow that here.
    # Disable late_binding, so the value is available immediately in before_binding.
    SENTRY_DSN = values.Value(None, environ_prefix=None, late_binding=False)

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        try:
            import sentry_sdk
        except ImportError:
            # If "sentry-sdk" is not installed, do not proceed
            return

        # These should always succeed, if the package is installed
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        integrations = [
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
        ]

        try:
            from sentry_sdk.integrations.celery import CeleryIntegration
        except sentry_sdk.integrations.DidNotEnable:
            # If "celery" is not installed, we can still proceed without that integration
            pass
        else:
            integrations.append(CeleryIntegration())

        sentry_sdk.init(
            # Even if a "dsn" is not explicitly passed, sentry_sdk will attempt to find the DSN in
            # the SENTRY_DSN environment variable; however, by making it an explicit setting,
            # it can be overridden by subclasses
            dsn=configuration.SENTRY_DSN,
            integrations=integrations,
            # Send traces for non-exception events too
            attach_stacktrace=True,
            # Submit request User info from Django
            send_default_pii=True,
        )
