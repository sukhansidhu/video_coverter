import os
import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters

from config import Config
from utils.ffmpeg import edit_metadata
from utils.helpers import get_media_info, generate_unique_filename
from utils.buttons import metadata_editor_keyboard, progress_keyboard, cancel_keyboard
from utils.progress_tracker import ProgressTracker

logger = logging.getLogger(__name__)

# Step 1: Ask user for a video file
async def start_metadata_editor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📝 Metadata Editor\n\nPlease send a video file to proceed.",
        reply_markup=cancel_keyboard()
    )
    context.user_data['expecting'] = 'metadata_video'

# Step 2: Download the video with progress UI
async def process_metadata_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data.get('expecting') != 'metadata_video':
        return

    video = update.message.video
    if not video:
        await update.message.reply_text("❌ Please send a valid video file.")
        return

    os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(Config.METADATA_DIR, exist_ok=True)

    progress_msg = await update.message.reply_text(
        "📥 Downloading Video...",
        reply_markup=progress_keyboard()
    )

    video_file = await video.get_file()
    video_path = os.path.join(Config.DOWNLOAD_PATH, f"{video.file_id}.mp4")

    tracker = ProgressTracker(
        video_path,
        video_file.file_size,
        update,
        context,
        progress_msg.message_id
    )

    await video_file.download_to_drive(
        video_path,
        progress=tracker.update_progress
    )

    tracker.complete()
    user_data['video_path'] = video_path

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
    context.user_data.pop('expecting', None)
    context.user_data['expecting'] = 'metadata_edit'

    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=progress_msg.message_id,
        text="✅ Video downloaded.\n\nSelect a stream to edit:",
        reply_markup=metadata_editor_keyboard(streams)
    )

# Step 3: Handle button clicks to edit metadata
async def handle_metadata_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_data = context.user_data
    streams = user_data.get('streams', [])

    if data == "show_progress":
        await query.edit_message_text("⏳ Downloading video...", reply_markup=progress_keyboard())

    elif data == "cancel_download":
        await query.delete_message()
        user_data.clear()

    elif data.startswith("edit_stream_"):
        stream_id = int(data.split("_")[2])
        stream = next((s for s in streams if s['id'] == stream_id), None)
        if stream:
            user_data['current_stream'] = stream_id
            await query.edit_message_text(
                "🎯 Editing stream metadata:\n\n"
                "Send *just the title* (ex: `My New Title`), or\n"
                "Send *title + language* (ex: `My Title | eng`)",
                parse_mode='Markdown'
            )

    elif data == "edit_all_streams":
        await query.edit_message_text(
            "📝 Send metadata for all streams:\n\n"
            "`stream_index|title|language`\n"
            "Separate by new lines.\n\n"
            "*Example:*\n"
            "0|Main Video|und\n"
            "1|English Audio|eng\n"
            "2|Subs|eng",
            parse_mode='Markdown'
        )
        user_data['expecting'] = 'all_metadata'

    elif data == "upload_video":
        video_path = user_data.get('video_path')
        if not video_path:
            await query.edit_message_text("⚠️ Video not found.")
            return

        await query.edit_message_text("⏳ Processing and uploading...")

        output_path = os.path.join(
            Config.UPLOAD_PATH,
            generate_unique_filename(Config.UPLOAD_PATH, os.path.basename(video_path))
        )

        if edit_metadata(video_path, output_path, streams):
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=open(output_path, 'rb'),
                caption="✅ Here's your video with edited metadata!"
            )
        else:
            await query.edit_message_text("❌ Failed to process metadata.")
        
        user_data.clear()

# Step 4: Handle user text input for metadata
async def process_metadata_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    expecting = user_data.get('expecting')
    if not expecting:
        return

    text = update.message.text.strip()
    streams = user_data.get('streams', [])

    if expecting == 'metadata_edit':
        stream_id = user_data.get('current_stream')
        stream = next((s for s in streams if s['id'] == stream_id), None)
        if stream:
            if '|' in text:
                title, lang = text.split('|', 1)
                stream['title'] = title.strip()
                stream['language'] = lang.strip()
            else:
                stream['title'] = text
            await update.message.reply_text(
                f"✅ Updated Stream {stream_id}:\nTitle: {stream['title']}\nLanguage: {stream['language']}"
            )

    elif expecting == 'all_metadata':
        for line in text.splitlines():
            try:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    stream_id = int(parts[0])
                    stream = next((s for s in streams if s['id'] == stream_id), None)
                    if stream:
                        stream['title'] = parts[1]
                        if len(parts) > 2:
                            stream['language'] = parts[2]
            except Exception as e:
                logger.warning(f"Invalid metadata line: {line} - {e}")
                continue
        await update.message.reply_text("✅ All stream metadata updated!")

    user_data.pop('expecting', None)

# Register all metadata handlers
def setup_metadata_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_metadata_actions, pattern="^(edit_stream_|edit_all_streams|upload_video|show_progress|cancel_download)$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_metadata_edit))
    application.add_handler(MessageHandler(filters.VIDEO, process_metadata_video))
