import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from utils.buttons import caption_editor_keyboard, cancel_keyboard

logger = logging.getLogger(__name__)

# Entry point for the caption editor menu
async def handle_caption_editor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📝 Caption and Buttons Editor\n\nSelect an option:",
        reply_markup=caption_editor_keyboard()
    )
    context.user_data['caption_edit'] = True

# Handle all inline button actions
async def handle_caption_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    match data:
        case "caption_Add_Caption":
            await query.edit_message_text(
                "✍️ Please send the new caption:",
                reply_markup=cancel_keyboard()
            )
            context.user_data['expecting'] = 'new_caption'

        case "caption_Remove_Caption":
            await query.edit_message_text("🗑️ Caption removed successfully!")

        case "caption_Add_Button":
            await query.edit_message_text(
                "🔘 Please send button text and URL in format: `Button Text|URL`",
                reply_markup=cancel_keyboard()
            )
            context.user_data['expecting'] = 'new_button'

        case "caption_Remove_Button":
            await query.edit_message_text("🗑️ Buttons removed successfully!")

        case "caption_Add_New_Caption":
            await query.edit_message_text(
                "✏️ Please send the new caption:",
                reply_markup=cancel_keyboard()
            )
            context.user_data['expecting'] = 'replace_caption'

        case "caption_Forward_Button":
            await query.edit_message_text("📤 Forward button added successfully!")

        case "caption_Back":
            await query.edit_message_text(
                "📝 Caption and Buttons Editor\n\nSelect an option:",
                reply_markup=caption_editor_keyboard()
            )

        case "caption_Cancel":
            await query.delete_message()

# Handle user text input based on what was expected
async def process_caption_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    expecting = user_data.get('expecting')

    if not expecting:
        return

    text = update.message.text.strip()

    if expecting == 'new_caption':
        await update.message.reply_text(f"✅ Caption added:\n\n{text}")

    elif expecting == 'replace_caption':
        await update.message.reply_text(f"🔄 Caption replaced:\n\n{text}")

    elif expecting == 'new_button':
        if '|' in text:
            btn_text, url = text.split('|', 1)
            await update.message.reply_text(f"✅ Button added:\n[{btn_text}]({url})", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Invalid format.\nUse: `Button Text|URL`", parse_mode='Markdown')

    user_data.pop('expecting', None)

# Register all caption editor handlers
def setup_caption_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_caption_actions, pattern="^caption_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_caption_input))
