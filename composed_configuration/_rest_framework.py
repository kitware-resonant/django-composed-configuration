from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class RestFrameworkMixin(ConfigMixin):
    """
    Configure Django REST Framework.

    This requires the `django-cors-headers` and `drf-yasg` packages to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += ['rest_framework', 'rest_framework.authtoken', 'drf_yasg']

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ]
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
