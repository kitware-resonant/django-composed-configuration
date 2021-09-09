from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class GirderUtilsMixin(ConfigMixin):
    """
    Configure girder_utils template tags.

    This requires the `django-girder-utils` package to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += ['girder_utils']
