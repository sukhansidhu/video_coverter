import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")
    UPLOAD_PATH = os.getenv("UPLOAD_PATH", "uploads")
    MAX_TITLE_LENGTH = int(os.getenv("MAX_TITLE_LENGTH", 10))
    ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").split(",") if os.getenv("ALLOWED_USERS") else []
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 2000 * 1024 * 1024))
    THUMBNAIL_DIR = os.getenv("THUMBNAIL_DIR", "thumbnails")
    METADATA_DIR = os.getenv("METADATA_DIR", "metadata")
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
    
