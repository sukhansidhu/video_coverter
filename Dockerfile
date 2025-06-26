FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements.txt from root
COPY requirements.txt /app/requirements.txt

# Copy bot code from /bot into /app
COPY bot/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
