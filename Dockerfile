FROM python:3.13-slim

WORKDIR /app


# Install redis server
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
    
COPY start.sh .

RUN chmod +x start.sh

COPY . .


CMD redis-server --daemonize yes && \
    python worker.py & \
    uvicorn main:app --host 0.0.0.0 --port 8000