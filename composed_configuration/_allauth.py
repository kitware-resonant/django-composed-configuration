from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class AllauthMixin(ConfigMixin):
    """
    Configure Django Allauth.

    This requires the django-allauth and django-material packages to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += [
            'django.contrib.sites',
            'composed_configuration.authentication',
            'allauth',
            'allauth.account',
            'allauth.socialaccount',
            'allauth.socialaccount.providers.google',
            'material',
        ]

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    # see configuration documentation at
    #   https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_ADAPTER = 'composed_configuration.authentication.adapter.EmailAsUsernameAccountAdapter'
    ACCOUNT_LOGOUT_ON_GET = True
    ACCOUNT_CONFIRM_EMAIL_ON_GET = True
    ACCOUNT_PRESERVE_USERNAME_CASING = False
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
    ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

    # should be overridden by downstream projects to point to valid urls
    LOGIN_REDIRECT_URL = '/'
    ACCOUNT_LOGOUT_REDIRECT_URL = '/'
