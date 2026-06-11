from redis import Redis
from rq import Queue

redis_conn = Redis(host="redis", port=6379, db=0)

review_queue = Queue(
    "reviews",
    connection=redis_conn,
)
