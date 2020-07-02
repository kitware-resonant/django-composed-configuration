from urllib.parse import urlsplit, urlunsplit

from django.utils.deconstruct import deconstructible
from minio_storage.storage import MinioMediaStorage, MinioStorage


class _BaseUrlMinioMixin:
    def __init__(self):
        super().__init__()
        self._fix_base_url()

    def _fix_base_url(self):
        if not self.base_url:
            # If base_url is not active or this function has already been called
            return

        # Strip the path from base_url, as it typically contains a bucket path
        base_url_parts = urlsplit(self.base_url)
        base_url_endpoint = urlunsplit((base_url_parts.scheme, base_url_parts.netloc, '', '', ''))

        # Abuse the enable_s3_accelerate feature of Minio to change which host signed requests
        # are generated for.
        # At this time, the enable_s3_accelerate feature is only used by "Minio.presigned_url".
        self.client._enable_s3_accelerate = True
        self.client._accelerate_endpoint_url = base_url_endpoint

        # Disable MinioStorage's attempt to replace parts of the URL after it's generated
        self.base_url = None


@deconstructible
class BaseUrlMinioStorage(_BaseUrlMinioMixin, MinioStorage):
    pass


@deconstructible
class BaseUrlMinioMediaStorage(_BaseUrlMinioMixin, MinioMediaStorage):
    pass
