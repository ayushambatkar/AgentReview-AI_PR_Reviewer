from redis import Redis
from rq import Queue
from src.core.config import settings

redis_conn = Redis(host=settings.redis_host, port=settings.redis_port, db=0)

review_queue = Queue(
    "reviews",
    connection=redis_conn,
)
