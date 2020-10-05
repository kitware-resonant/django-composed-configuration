from typing import Type

from ._base import ComposedConfiguration, ConfigMixin


class DebugMixin(ConfigMixin):
    """
    Configure debug tooling.

    This requires the `django-debug-toolbar` package to be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += ['debug_toolbar']

        # Include Debug Toolbar middleware as early as possible in the list.
        # However, it must come after any other middleware that encodes the response’s content,
        # such as GZipMiddleware.
        configuration.MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    # SHOW_TOOLBAR_CALLBACK for debug_toolbar normally relies on INTERNAL_IPS, but force enable
    # it to support running Django inside Docker (where the host's real IP is unknown)
    @property
    def DEBUG_TOOLBAR_CONFIG(self):  # noqa: N802
        # For extra safety, only enable when also in debug mode, though normally, DebugMixin is not
        # included in a production configuration
        # Only lookup the DEBUG setting once, instead of on every callback
        debug = self.DEBUG
        return {
            'SHOW_TOOLBAR_CALLBACK': lambda request: debug,
        }
