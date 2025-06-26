import time
import os
from config import Config
from utils.helpers import get_file_size

class ProgressTracker:
    def __init__(self, file_path, total_size, update, context, message_id):
        self.file_path = file_path
        self.total_size = total_size
        self.update = update
        self.context = context
        self.message_id = message_id
        self.start_time = time.time()
        self.last_update_time = 0
        self.downloaded = 0
        self.cancelled = False
        self.completed = False

    def update_progress(self, chunk_size):
        self.downloaded += chunk_size
        current_time = time.time()

        # Only update every 1 second
        if current_time - self.last_update_time < 1:
            return

        percentage = (self.downloaded / self.total_size) * 100
        elapsed_time = current_time - self.start_time
        speed = self.downloaded / elapsed_time if elapsed_time > 0 else 0
        remaining = self.total_size - self.downloaded
        time_left = remaining / speed if speed > 0 else 0

        # Build visual progress bar
        filled = int(percentage / 5)
        empty = 20 - filled
        progress_bar = '▰' * filled + '▱' * empty

        text = (
            "📥 <b>Downloading Video</b>\n"
            "🔄 <i>From: DC1</i>\n\n"
            f"<code>{progress_bar}</code>\n\n"
            f"✅ Downloaded: <b>{get_file_size(self.downloaded)} / {get_file_size(self.total_size)}</b>\n"
            f"🚀 Speed: <b>{get_file_size(speed)}/s</b>\n"
            f"⏳ ETA: <b>{time_left:.1f} seconds</b>\n\n"
            "Please wait..."
        )

        try:
            self.context.bot.edit_message_text(
                chat_id=self.update.effective_chat.id,
                message_id=self.message_id,
                text=text,
                parse_mode='HTML'
            )
        except Exception as e:
            pass  # Avoid flooding logs or halting on edit errors

        self.last_update_time = current_time

    def complete(self):
        self.completed = True
        try:
            self.context.bot.edit_message_text(
                chat_id=self.update.effective_chat.id,
                message_id=self.message_id,
                text="✅ Download completed. Processing video now..."
            )
        except Exception:
            pass
