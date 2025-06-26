import os
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config import Config
from utils.ffmpeg import extract_thumbnail
from utils.buttons import cancel_keyboard

logger = logging.getLogger(__name__)

async def handle_thumbnail_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Please send a video to extract thumbnail from:",
        reply_markup=cancel_keyboard()
    )
    context.user_data['expecting'] = 'thumbnail_video'

async def process_thumbnail_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data.get('expecting') != 'thumbnail_video':
        return
    
    video = update.message.video
    if not video:
        await update.message.reply_text("Please send a valid video file.")
        return
    
    # Get absolute paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(base_dir, Config.DOWNLOAD_PATH)
    thumbnail_dir = os.path.join(base_dir, Config.THUMBNAIL_DIR)
    
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(thumbnail_dir, exist_ok=True)
    
    # Download video
    video_file = await video.get_file()
    video_path = os.path.join(download_path, video_file.file_id + ".mp4")
    await video_file.download_to_drive(video_path)
    
    # Extract thumbnail
    thumbnail_path = extract_thumbnail(video_path, thumbnail_dir)
    
    if thumbnail_path:
        await update.message.reply_photo(
            photo=open(thumbnail_path, 'rb'),
            caption="Here's your thumbnail!"
        )
    else:
        await update.message.reply_text("Failed to extract thumbnail. Please try another video.")
    
    user_data.pop('expecting', None)

def setup_thumbnail_handlers(application):
    application.add_handler(MessageHandler(filters.VIDEO & ~filters.COMMAND, process_thumbnail_video))
