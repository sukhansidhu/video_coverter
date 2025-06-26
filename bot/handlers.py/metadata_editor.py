import os
import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from config import Config
from utils.ffmpeg import edit_metadata
from utils.helpers import get_media_info, get_file_size, generate_unique_filename
from utils.buttons import metadata_editor_keyboard, progress_keyboard, cancel_keyboard
from utils.progress_tracker import ProgressTracker

logger = logging.getLogger(__name__)

async def start_metadata_editor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Metadata Editor\n\n"
        "Please send a video file:",
        reply_markup=cancel_keyboard()
    )
    context.user_data['expecting'] = 'metadata_video'

async def process_metadata_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data.get('expecting') != 'metadata_video':
        return
    
    video = update.message.video
    if not video:
        await update.message.reply_text("Please send a valid video file.")
        return
    
    # Create directories
    os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(Config.METADATA_DIR, exist_ok=True)
    
    # Show progress message
    progress_msg = await update.message.reply_text(
        "Downloading Video File",
        reply_markup=progress_keyboard()
    )
    
    # Download video with progress tracking
    video_file = await video.get_file()
    video_path = os.path.join(Config.DOWNLOAD_PATH, video_file.file_id + ".mp4")
    
    tracker = ProgressTracker(
        video_path,
        video_file.file_size,
        update,
        context,
        progress_msg.message_id
    )
    
    await video_file.download_to_drive(
        video_path,
        read_timeout=None,
        write_timeout=None,
        connect_timeout=None,
        pool_timeout=None,
        progress=tracker.update_progress
    )
    
    tracker.complete()
    user_data['video_path'] = video_path
    
    # Get media info
    media_info = get_media_info(video_path)
    streams = []
    stream_id = 0
    
    if 'video' in media_info:
        streams.append({
            "id": stream_id,
            "type": "video",
            "codec": media_info['video']['codec'],
            "language": "None",
            "title": "Video Stream"
        })
        stream_id += 1
    
    for audio in media_info.get('audio', []):
        streams.append({
            "id": stream_id,
            "type": "audio",
            "codec": audio['codec'],
            "language": audio['language'],
            "title": audio['title']
        })
        stream_id += 1
    
    for subtitle in media_info.get('subtitle', []):
        streams.append({
            "id": stream_id,
            "type": "subtitle",
            "codec": subtitle['codec'],
            "language": subtitle['language'],
            "title": subtitle['title']
        })
        stream_id += 1
    
    context.user_data['streams'] = streams
    
    # Show stream selection
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=progress_msg.message_id,
        text="Select Your Required Option",
        reply_markup=metadata_editor_keyboard(streams)
    )
    
    user_data.pop('expecting', None)
    user_data['expecting'] = 'metadata_edit'

async def handle_metadata_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    user_data = context.user_data
    streams = user_data.get('streams', [])
    
    if data == "show_progress":
        await query.edit_message_text(
            "Downloading Video File",
            reply_markup=progress_keyboard()
        )
    elif data == "cancel_download":
        await query.delete_message()
        user_data.clear()
    elif data.startswith("edit_stream_"):
        stream_id = int(data.split("_")[2])
        stream = next((s for s in streams if s['id'] == stream_id), None)
        
        if stream:
            user_data['current_stream'] = stream_id
            await query.edit_message_text(
                "For editing stream metadata (only Title), Just send title. ex. My New Title\n\n"
                "For editing stream metadata (Title And Language).\n"
                "Format - Your Audio Title | Language code\n\n"
                "Examples:\n"
                "For English Audio - Audio Title | eng\n\n"
                "Now send Title and Language for Audio"
            )
    elif data == "edit_all_streams":
        await query.edit_message_text(
            "Send new metadata for all streams in the format:\n"
            "stream_index|title|language\n"
            "Separate multiple streams with new lines\n\n"
            "Example:\n"
            "0|New Video Title|eng\n"
            "1|Main Audio|en\n"
            "2|English Subtitles|eng"
        )
        user_data['expecting'] = 'all_metadata'
    elif data == "upload_video":
        video_path = user_data.get('video_path')
        if video_path:
            await query.edit_message_text("Processing...")
            output_path = os.path.join(Config.UPLOAD_PATH, generate_unique_filename(
                Config.UPLOAD_PATH, os.path.basename(video_path))
            )
            
            if edit_metadata(video_path, output_path, streams):
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=open(output_path, 'rb'),
                    caption="Here's your video with edited metadata!"
                )
            else:
                await query.edit_message_text("Failed to edit metadata.")
        else:
            await query.edit_message_text("Video not found.")
        
        user_data.clear()

async def process_metadata_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    expecting = user_data.get('expecting')
    
    if not expecting:
        return
    
    text = update.message.text
    streams = user_data.get('streams', [])
    
    if expecting == 'metadata_edit':
        stream_id = user_data.get('current_stream')
        if stream_id is not None:
            stream = next((s for s in streams if s['id'] == stream_id), None)
            if stream:
                if '|' in text:
                    title, lang = text.split('|', 1)
                    stream['title'] = title.strip()
                    stream['language'] = lang.strip()
                else:
                    stream['title'] = text.strip()
                
                await update.message.reply_text(
                    f"Stream {stream_id} updated:\n"
                    f"Title: {stream['title']}\n"
                    f"Language: {stream['language']}"
                )
    elif expecting == 'all_metadata':
        for line in text.split('\n'):
            parts = line.split('|')
            if len(parts) >= 2:
                try:
                    stream_id = int(parts[0].strip())
                    title = parts[1].strip()
                    language = parts[2].strip() if len(parts) > 2 else None
                    
                    stream = next((s for s in streams if s['id'] == stream_id), None)
                    if stream:
                        stream['title'] = title
                        if language:
                            stream['language'] = language
                except (ValueError, IndexError):
                    continue
        
        await update.message.reply_text("All streams metadata updated!")
    
    user_data.pop('expecting', None)

def setup_metadata_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_metadata_actions))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_metadata_edit))
