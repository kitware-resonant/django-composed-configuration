from ._base import ConfigMixin


class LoggingMixin(ConfigMixin):
    """
    Configure Django logging.

    This causes the logger to ...
    """

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            # Based on https://stackoverflow.com/a/20983546
            # TODO: Do we like this format?
            'verbose': {
                'format': (
                    '%(asctime)s [%(process)d] [%(levelname)s] '
                    + 'pathname=%(pathname)s lineno=%(lineno)s '
                    + 'funcname=%(funcName)s %(message)s'
                ),
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                # Unlike the Django default "console" handler, this works during production,
                # has a level of DEBUG, and uses a different formatter
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'mail_admins': {
                # Disable Django's default "mail_admins" handler
                'class': 'logging.NullHandler',
            },
        },
    }
