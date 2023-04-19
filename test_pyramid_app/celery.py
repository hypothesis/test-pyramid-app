from os import environ
from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger
from kombu import Exchange, Queue

app = Celery("hello", broker=environ["BROKER_URL"])
app.conf.update(
    task_queues=[
        Queue(
            "celery",
            durable=True,
            routing_key="celery",
            exchange=Exchange("celery", durable=True),
        )
    ]
)

logger = get_task_logger(__name__)


@app.task(acks_late=True)
def work(seconds):  # pragma: no cover
    for second in reversed(range(seconds)):
        logger.info("Working %i", second + 1)
        sleep(1)
    logger.info("Finished working")
