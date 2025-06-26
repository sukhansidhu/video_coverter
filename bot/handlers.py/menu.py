from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from utils.buttons import main_menu_keyboard
from .thumbnail_extractor import handle_thumbnail_request
from .caption_editor import handle_caption_editor
from .metadata_editor import start_metadata_editor

# Callback handler for main menu and subfeatures
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data

    if data == "Menu":
        await query.edit_message_text(
            "📋 Main Menu\n\nPlease select an option:",
            reply_markup=main_menu_keyboard()
        )

    elif data == "Thumbnail Extractor":
        await handle_thumbnail_request(update, context)

    elif data == "Caption And Buttons Editor":
        await handle_caption_editor(update, context)

    elif data == "Metadata Editor":
        await start_metadata_editor(update, context)

    elif data == "Cancel X":
        await query.delete_message()

# Register the menu callback
def setup_menu_handlers(application):
    application.add_handler(CallbackQueryHandler(menu_callback))
