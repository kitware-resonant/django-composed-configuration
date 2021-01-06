from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class RestFrameworkMixin(ConfigMixin):
    """
    Configure Django REST Framework.

    This requires the `django-cors-headers`, `django-girder-utils`, `django-oauth-toolkit`,
    and `drf-yasg` packages to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += [
            'rest_framework',
            'rest_framework.authtoken',
            'oauth2_provider',
            'drf_yasg',
        ]

        if configuration.DEBUG:
            configuration.OAUTH2_PROVIDER['ALLOWED_REDIRECT_URI_SCHEMES'] = ['http', 'https']
            # In development, always present the approval dialog
            configuration.OAUTH2_PROVIDER['REQUEST_APPROVAL_PROMPT'] = 'force'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            # Allow BasicAuthentication, for continued use with CLI clients and Swagger, until
            # OAuth can support both.
            'rest_framework.authentication.BasicAuthentication',
        ],
        # BoundedLimitOffsetPagination provides LimitOffsetPagination with a maximum page size
        'DEFAULT_PAGINATION_CLASS': 'girder_utils.rest_framework.BoundedLimitOffsetPagination',
        # This provides a sane default for requests that do not specify a page size.
        # This also ensures that endpoints with pagination will always return a
        # pagination-structured response.
        'PAGE_SIZE': 100,
    }

    OAUTH2_PROVIDER = {
        'PKCE_REQUIRED': True,
        'ALLOWED_REDIRECT_URI_SCHEMES': ['https'],
        # Don't require users to re-approve scopes each time
        'REQUEST_APPROVAL_PROMPT': 'auto',
        # ERROR_RESPONSE_WITH_SCOPES is only used with the "permission_classes" helpers for scopes.
        # If the scope itself is confidential, this could leak information. but the usability
        # benefit is probably worth it.
        'ERROR_RESPONSE_WITH_SCOPES': True,
        # Django can persist logins for longer than this via cookies,
        # but non-refreshing clients will need to redirect to Django's auth every 24 hours.
        'ACCESS_TOKEN_EXPIRE_SECONDS': 24 * 60 * 60,
        # This allows refresh tokens to eventually be removed from the database by
        # "manage.py cleartokens". This value is not actually enforced when refresh tokens are
        # checked, but it can be assumed that all clients will need to redirect to Django's auth
        # every 30 days.
        'REFRESH_TOKEN_EXPIRE_SECONDS': 30 * 24 * 60 * 60,
    }

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Basic': {'type': 'basic'},
        }
    }

    REDOC_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Basic': {'type': 'basic'},
        }
    }
