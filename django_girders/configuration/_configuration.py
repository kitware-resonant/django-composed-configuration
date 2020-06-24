from configurations import values

from ._base import ComposedConfiguration
from ._celery import CeleryMixin
from ._cors import CorsMixin
from ._database import DatabaseMixin
from ._debug import DebugMixin
from ._django import DjangoMixin
from ._email import EmailMixin
from ._extensions import ExtensionsMixin
from ._logging import LoggingMixin
from ._rest_framwork import RestFrameworkMixin
from ._static import WhitenoiseStaticFileMixin
from ._storage import MinioStorageMixin


# Subclasses are loaded in last to first ordering
class _BaseConfiguration(
    ExtensionsMixin,
    CeleryMixin,
    RestFrameworkMixin,
    # CorsMixin must be loaded after WhitenoiseStaticFileMixin
    CorsMixin,
    WhitenoiseStaticFileMixin,
    DatabaseMixin,
    EmailMixin,
    LoggingMixin,
    # DjangoMixin should be loaded first
    DjangoMixin,
    ComposedConfiguration,
):
    pass


class DevelopmentBaseConfiguration(DebugMixin, MinioStorageMixin, _BaseConfiguration):
    DEBUG = True
    SECRET_KEY = 'insecuresecret'
    ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1'])
    CORS_ORIGIN_REGEX_WHITELIST = values.ListValue(
        [r'^https?://localhost:\d+$', r'^https?://127\.0\.0\.1:\d+$']
    )

    # INTERNAL_IPS does not work properly when this is run within Docker, since the bridge
    # sends requests from the host machine via a dedicated IP address
    INTERNAL_IPS = ['127.0.0.1']
