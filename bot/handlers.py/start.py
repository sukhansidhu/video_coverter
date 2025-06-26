from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name or 'there'}!\n\n"
        "I'm your media toolkit bot. Use the menu to get started editing videos, thumbnails, metadata, and more!"
    )

def setup_start_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
