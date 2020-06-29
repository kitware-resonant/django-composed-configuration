from typing import cast, Dict, Type

from configurations import values

from ._base import ComposedConfiguration, ConfigMixin


class EmailMixin(ConfigMixin):
    """
    Configure Django's email sending.

    The `DJANGO_EMAIL_URL` environment variable must be externally set
    to a URL for login to an STMP server, as parsed by `dj-email-url`. This
    typically will start with `submission:`. Special characters in passwords must
    be URL-encoded. See https://pypi.org/project/dj-email-url/ for full details.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        email = cast(
            Dict[str, str],
            values.EmailURLValue(
                environ_name='EMAIL_URL',
                environ_prefix='DJANGO',
                # Disable late_binding, to make this return a usable value (which is a simple dict)
                # immediately
                late_binding=False,
            ),
        )
        for email_setting, email_setting_value in email.items():
            setattr(configuration, email_setting, email_setting_value)
