from rq import Worker, Queue
from redis import Redis
from src.core.queue import review_queue, redis_conn


worker = Worker([review_queue], connection=redis_conn)

worker.work()