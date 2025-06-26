FROM python:3.10-slim-buster

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full app into /app
COPY . .

# Create necessary folders
RUN mkdir -p bot/downloads bot/uploads bot/thumbnails bot/metadata

# Set working directory to the folder containing main.py
WORKDIR /app/bot

# Run the bot
CMD ["python", "main.py"]
