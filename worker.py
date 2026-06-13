import os

from rq import SimpleWorker, Worker

from src.core.queue import redis_conn, review_queue
from src.core.config import settings

def create_worker():
	if os.name == "nt":
		print(settings.langchain_api_key)
		print(settings.langchain_project)
		print("LANGCHAIN_TRACING_V2 =", os.getenv("LANGCHAIN_TRACING_V2"))
		print("LANGCHAIN_API_KEY exists =", bool(os.getenv("LANGCHAIN_API_KEY")))
		return SimpleWorker([review_queue], connection=redis_conn)

	return Worker([review_queue], connection=redis_conn)


if __name__ == "__main__":
	worker = create_worker()
	worker.work()