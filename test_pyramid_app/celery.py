from os import environ
from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger

app = Celery("hello", broker=environ["BROKER_URL"])
app.conf.update(
    # Tell Celery to kill any task run (by raising
    # celery.exceptions.SoftTimeLimitExceeded) if it takes longer than
    # task_soft_time_limit seconds.
    #
    # See: https://docs.celeryq.dev/en/stable/userguide/workers.html#time-limits
    #
    # This is to protect against task runs hanging forever which blocks a
    # Celery worker and prevents Celery retries from kicking in.
    #
    # This can be overridden on a per-task basis by adding soft_time_limit=n to
    # the task's @app.task() arguments.
    #
    # We're using soft rather than hard time limits because hard time limits
    # don't trigger Celery retries whereas soft ones do. Soft time limits also
    # give the task a chance to catch SoftTimeLimitExceeded and do some cleanup
    # before exiting.
    task_soft_time_limit=3600,
    # Tell Celery to force-terminate any task run (by terminating the worker
    # process and replacing it with a new one) if it takes linger than
    # task_time_limit seconds.
    #
    # This is needed to defend against tasks hanging during cleanup: if
    # task_soft_time_limit expires the task can catch SoftTimeLimitExceeded and
    # could then hang again in the exception handler block. task_time_limit
    # ensures that the task is force-terminated in that case.
    #
    # This can be overridden on a per-task basis by adding time_limit=n to the
    # task's @app.task() arguments.
    task_time_limit=7200,
    # Disable Celery task rate limits in local development.
    worker_disable_rate_limits=environ.get("DEV") == "true",
)

logger = get_task_logger(__name__)


@app.task(acks_late=True, autoretry_for=(Exception,), max_retries=2)
def work(seconds):  # pragma: no cover
    for second in reversed(range(seconds)):
        logger.info("Working %i", second + 1)
        sleep(1)
    logger.info("Finished working")
