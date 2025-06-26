FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Copy everything from `bot/` (where handlers/ and main.py live) into /app
COPY bot/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
