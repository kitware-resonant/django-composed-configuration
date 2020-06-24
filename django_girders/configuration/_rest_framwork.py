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
        'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication']
    }
