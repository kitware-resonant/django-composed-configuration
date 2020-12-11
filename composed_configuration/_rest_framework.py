from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class RestFrameworkMixin(ConfigMixin):
    """
    Configure Django REST Framework.

    This requires the `django-cors-headers` and `drf-yasg2` packages to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += ['rest_framework', 'rest_framework.authtoken', 'drf_yasg2']

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
        # This provides a sane default for requests that do not specify a page size.
        # This also ensures that endpoints with pagination will always return a
        # pagination-structured response.
        'PAGE_SIZE': 100,
    }

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Basic': {'type': 'basic'},
            'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
        }
    }

    REDOC_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Basic': {'type': 'basic'},
            'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
        }
    }
