from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Progress is handled in ProgressTracker

def setup_progress_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_progress, pattern="^(show_progress|cancel_download)$"))
