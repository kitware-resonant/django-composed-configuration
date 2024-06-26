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
    CELERY_BROKER_URL = values.Value("amqp://localhost:5672/")

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

    # When a worker subprocess abruptly exists, assume it was is killed by the operating system for
    # a cause which is intrinsic (e.g. a segfault or OOM) to the task it was running, so do not
    # requeue. It's expected that the task wouldn't succeed if run again.
    # This should not impact cases where the task fails due to extrinsic causes (e.g. the process
    # supervisor sends a SIGKILL or the machine loses power), as we assume that the parent worker
    # process will immediately die too (and not have a chance to requeue the task).
    # See: https://docs.celeryproject.org/en/stable/userguide/tasks.html#tasks for more explanation
    # of these tradeoffs.
    # None of this affects warm shutdowns from a SIGTERM (which the process supervisor ought to
    # send), as this just allows Celery to complete running tasks; see:
    # https://docs.celeryproject.org/en/stable/userguide/workers.html#process-signals for reference.
    # This is Celery's default.
    CELERY_TASK_REJECT_ON_WORKER_LOST = False

    # When a task fails due to an internally-raised exception or due to a timeout, do not requeue.
    # It's expected that the task wouldn't succeed if run again.
    # This is Celery's default.
    CELERY_TASK_ACKS_ON_FAILURE_OR_TIMEOUT = True

    # This is sensible behavior with TASKS_ACKS_LATE, this must be enabled to prevent warnings,
    # and this will be Celery's default in 6.0.
    CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS = True

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
