FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BOT_TOKEN=$BOT_TOKEN

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p bot/downloads bot/uploads bot/thumbnails bot/metadata

CMD ["python", "bot/main.py"]
