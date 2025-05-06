from celery import Celery

from core.config import config


celery_app = Celery(
    main="worker",
    broker=config.redis.url_broker,
    backend=config.redis.url_backend,
)

celery_app.conf.update(broker_connection_retry_on_startup=True)
