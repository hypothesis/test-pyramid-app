from os import environ
from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger

app = Celery("hello", broker=environ["BROKER_URL"])

logger = get_task_logger(__name__)


@app.task
def work(seconds):  # pragma: no cover
    for second in reversed(range(seconds)):
        logger.info("Working %i", second + 1)
        sleep(1)
    logger.info("Finished working")
