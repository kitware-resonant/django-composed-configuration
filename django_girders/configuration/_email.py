from ._base import ConfigMixin


class EmailMixin(ConfigMixin):
    """Configure Django's email sending."""

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
