from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.buttons import main_menu_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! Welcome to Media Bot.\n"
        "Please select an option from the menu below:",
        reply_markup=main_menu_keyboard()
    )

def setup_start_handlers(application):
    application.add_handler(CommandHandler("start", start))
