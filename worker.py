import os

from rq import SimpleWorker, Worker

from src.core.queue import redis_conn, review_queue


def create_worker():
	if os.name == "nt":
		return SimpleWorker([review_queue], connection=redis_conn)

	return Worker([review_queue], connection=redis_conn)


if __name__ == "__main__":
	worker = create_worker()
	worker.work()