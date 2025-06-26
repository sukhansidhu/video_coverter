FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY bot/ /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
