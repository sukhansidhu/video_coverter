import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Telegram bot token (must be set in .env or environment)
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set. Please set it in your .env file or environment variables.")

    # Directory paths
    DOWNLOAD_PATH = "downloads"
    UPLOAD_PATH = "uploads"
    THUMBNAIL_DIR = "thumbnails"
    METADATA_DIR = "metadata"

    # Limits and settings
    MAX_TITLE_LENGTH = 10
    MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2 GB

    # Optional: comma-separated user IDs in .env (e.g., ALLOWED_USERS=123456789,987654321)
    ALLOWED_USERS = list(map(int, os.getenv("ALLOWED_USERS", "").split(","))) if os.getenv("ALLOWED_USERS") else []

    # Path to FFmpeg binary
    FFMPEG_PATH = "ffmpeg"
