import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    DOWNLOAD_PATH = "downloads"
    UPLOAD_PATH = "uploads"
    MAX_TITLE_LENGTH = 10
    ALLOWED_USERS = []
    MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2GB
    THUMBNAIL_DIR = "thumbnails"
    METADATA_DIR = "metadata"
    FFMPEG_PATH = "ffmpeg"
