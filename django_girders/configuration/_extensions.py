from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class ExtensionsMixin(ConfigMixin):
    """
    Configure Django Extensions.

    This requires the `django-extensions` package to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += ['django_extensions']

    SHELL_PLUS_PRINT_SQL = True
