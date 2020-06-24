from configurations import values

from ._base import ConfigMixin


class CeleryMixin(ConfigMixin):
    """
    Configure Celery.

    The Celery app must be constructed as:
        app = Celery(
            '<my_project_name>',  # Change this
            config_source='django.conf:settings',
            namespace='CELERY'
        )

    The `DJANGO_CELERY_BROKER_URL` environment variable may be externally set to an AMQP URL.
    """

    # Assume AMQP.
    CELERY_BROKER_URL = values.Value('amqp://localhost:5672/')

    # Disable results backend, as this feature has too many weaknesses.
    # The database should be used to communicate results of completed tasks.
    CELERY_RESULT_BACKEND = None

    # Only acknowledge a task being done after the function finishes.
    # This provides safety against worker crashes, but adds the requirement
    # that tasks must be idempotent (which is a best practice anyway).
    # See: https://docs.celeryproject.org/en/stable/faq.html#should-i-use-retry-or-acks-late
    # Acknowledge early in development, which will help prevent failing or
    # long-running tasks from being started automatically every time the worker
    # process restarts; this more aggressively flushes the task queue.
    @property
    def CELERY_TASK_ACKS_LATE(self):  # noqa: N802
        return False if self.DEBUG else True

    # CloudAMQP-suggested settings
    # https://www.cloudamqp.com/docs/celery.html
    CELERY_BROKER_POOL_LIMIT = 1
    CELERY_BROKER_HEARTBEAT = None
    CELERY_BROKER_CONNECTION_TIMEOUT = 30
    CELERY_EVENT_QUEUE_EXPIRES = 60

    # Note, CELERY_WORKER settings could be different on each running worker.

    # Do not prefetch, as the speed benefit for fast-running tasks may not be
    # worth a potentially unfair allocation with slow-running tasks and
    # multiple workers.
    CELERY_WORKER_PREFETCH_MULTIPLIER = 1

    # In development, run without concurrency, otherwise accept the default of
    # the number of CPU cores.
    # Workers running memory-intensive tasks may need to decrease this.
    @property
    def CELERY_WORKER_CONCURRENCY(self):  # noqa: N802
        return 1 if self.DEBUG else None
