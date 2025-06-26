import logging
import os
from telegram.ext import Application
from .config import Config
from .handlers.start import setup_start_handlers
from .handlers.menu import setup_menu_handlers
from .handlers.thumbnail_extractor import setup_thumbnail_handlers
from .handlers.caption_editor import setup_caption_handlers
from .handlers.metadata_editor import setup_metadata_handlers
from .handlers.progress import setup_progress_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # Create directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, Config.DOWNLOAD_PATH), exist_ok=True)
    os.makedirs(os.path.join(base_dir, Config.UPLOAD_PATH), exist_ok=True)
    os.makedirs(os.path.join(base_dir, Config.THUMBNAIL_DIR), exist_ok=True)
    os.makedirs(os.path.join(base_dir, Config.METADATA_DIR), exist_ok=True)
    
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    setup_start_handlers(application)
    setup_menu_handlers(application)
    setup_thumbnail_handlers(application)
    setup_caption_handlers(application)
    setup_metadata_handlers(application)
    setup_progress_handlers(application)
    
    application.run_polling()

if __name__ == "__main__":
    main()
