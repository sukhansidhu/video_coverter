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
        current_time = time.time()
        self.downloaded += chunk_size
        
        # Update progress every 1 second
        if current_time - self.last_update_time >= 1:
            percentage = (self.downloaded / self.total_size) * 100
            elapsed_time = current_time - self.start_time
            speed = self.downloaded / elapsed_time if elapsed_time > 0 else 0
            remaining_bytes = self.total_size - self.downloaded
            time_left = remaining_bytes / speed if speed > 0 else 0
            
            progress_bar = '[' + '■' * int(percentage / 5) + '□' * (20 - int(percentage / 5)) + ']'
            text = (
                "Video Converter New\n\n"
                f"Downloading.... from DC1\n\n"
                f"{progress_bar}\n\n"
                f"Downloaded: {get_file_size(self.downloaded)} / {get_file_size(self.total_size)} ({percentage:.1f}%)\n"
                f"Speed: {get_file_size(speed)}/s\n"
                f"Time Left: {time_left:.1f}s\n\n"
                "OK"
            )
            
            try:
                self.context.bot.edit_message_text(
                    chat_id=self.update.effective_chat.id,
                    message_id=self.message_id,
                    text=text
                )
            except Exception:
                pass
            
            self.last_update_time = current_time

    def complete(self):
        self.completed = True
        text = "Processing time depends on file size. So please wait..."
        try:
            self.context.bot.edit_message_text(
                chat_id=self.update.effective_chat.id,
                message_id=self.message_id,
                text=text
            )
        except Exception:
            pass
