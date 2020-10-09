from typing import List

from configurations import values

from ._base import ComposedConfiguration
from ._celery import CeleryMixin
from ._cors import CorsMixin
from ._database import DatabaseMixin
from ._debug import DebugMixin
from ._django import DjangoMixin
from ._email import ConsoleEmailMixin, SmtpEmailMixin
from ._extensions import ExtensionsMixin
from ._filter import FilterMixin
from ._https import HttpsMixin
from ._logging import LoggingMixin
from ._rest_framework import RestFrameworkMixin
from ._sentry import SentryConfig
from ._static import WhitenoiseStaticFileMixin
from ._storage import MinioStorageMixin, S3StorageMixin


# Subclasses are loaded in last to first ordering
class _BaseConfiguration(
    ExtensionsMixin,
    CeleryMixin,
    RestFrameworkMixin,
    FilterMixin,
    # CorsMixin must be loaded after WhitenoiseStaticFileMixin
    CorsMixin,
    WhitenoiseStaticFileMixin,
    DatabaseMixin,
    LoggingMixin,
    # DjangoMixin should be loaded first
    DjangoMixin,
    ComposedConfiguration,
):
    pass


class DevelopmentBaseConfiguration(
    DebugMixin, ConsoleEmailMixin, MinioStorageMixin, _BaseConfiguration
):
    DEBUG = True
    SECRET_KEY = 'insecuresecret'

    ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1'])
    CORS_ORIGIN_REGEX_WHITELIST = values.ListValue(
        [r'^https?://localhost:\d+$', r'^https?://127\.0\.0\.1:\d+$']
    )
    # INTERNAL_IPS does not work properly when this is run within Docker, since the bridge
    # sends requests from the host machine via a dedicated IP address
    INTERNAL_IPS = ['127.0.0.1']

    # Setting this allows MinIO to work through network namespace partitions
    # (e.g. when running within Docker Compose)
    MINIO_STORAGE_MEDIA_URL = values.Value(None)


class TestingBaseConfiguration(MinioStorageMixin, _BaseConfiguration):
    SECRET_KEY = 'testingsecret'

    # Testing will add 'testserver' to ALLOWED_HOSTS
    ALLOWED_HOSTS: List[str] = []

    MINIO_STORAGE_MEDIA_BUCKET_NAME = 'test-django-storage'

    # Testing will set EMAIL_BACKEND to use the memory backend


class ProductionBaseConfiguration(
    SentryConfig, SmtpEmailMixin, S3StorageMixin, HttpsMixin, _BaseConfiguration
):
    pass


class HerokuProductionBaseConfiguration(ProductionBaseConfiguration):
    # Use different env var names (with no DJANGO_ prefix) for services that Heroku auto-injects
    DATABASES = values.DatabaseURLValue(
        environ_name='DATABASE_URL',
        environ_prefix=None,
        environ_required=True,
        engine='django.db.backends.postgresql',
        conn_max_age=600,
        ssl_require=True,
    )
    CELERY_BROKER_URL = values.Value(
        environ_name='CLOUDAMQP_URL', environ_prefix=None, environ_required=True
    )
    # https://help.heroku.com/J2R1S4T8/can-heroku-force-an-application-to-use-ssl-tls
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
