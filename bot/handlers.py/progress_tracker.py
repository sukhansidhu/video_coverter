import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

logger = logging.getLogger(__name__)

# Handle dummy callbacks for progress-related buttons
async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_data = context.user_data

    if data == "show_progress":
        await query.edit_message_text("⏳ Download in progress...")

    elif data == "cancel_download":
        await query.delete_message()
        user_data.clear()
        logger.info(f"User {update.effective_user.id} canceled the download.")

# Register handlers
def setup_progress_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_progress, pattern="^(show_progress|cancel_download)$"))
