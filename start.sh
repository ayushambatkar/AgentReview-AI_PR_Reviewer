#!/bin/sh

redis-server &
python worker.py &
uvicorn main:app --host 0.0.0.0 --port $PORT