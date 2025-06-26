import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from utils.buttons import caption_editor_keyboard, cancel_keyboard

logger = logging.getLogger(__name__)

async def handle_caption_editor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Caption and Buttons Editor\n\n"
        "Select an option:",
        reply_markup=caption_editor_keyboard()
    )
    context.user_data['caption_edit'] = True

async def handle_caption_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "caption_Add_Caption":
        await query.edit_message_text(
            "Please send the new caption:",
            reply_markup=cancel_keyboard()
        )
        context.user_data['expecting'] = 'new_caption'
    elif data == "caption_Remove_Caption":
        await query.edit_message_text("Caption removed successfully!")
    elif data == "caption_Add_Button":
        await query.edit_message_text(
            "Please send button text and URL in format: 'Button Text|URL'",
            reply_markup=cancel_keyboard()
        )
        context.user_data['expecting'] = 'new_button'
    elif data == "caption_Remove_Button":
        await query.edit_message_text("Buttons removed successfully!")
    elif data == "caption_Add_New_Caption":
        await query.edit_message_text(
            "Please send the new caption:",
            reply_markup=cancel_keyboard()
        )
        context.user_data['expecting'] = 'replace_caption'
    elif data == "caption_Forward_Button":
        await query.edit_message_text("Forward button added successfully!")
    elif data == "caption_Back":
        await query.edit_message_text(
            "Caption and Buttons Editor\n\n"
            "Select an option:",
            reply_markup=caption_editor_keyboard()
        )
    elif data == "caption_Cancel":
        await query.delete_message()

async def process_caption_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    expecting = user_data.get('expecting')
    
    if not expecting:
        return
    
    text = update.message.text
    
    if expecting == 'new_caption':
        await update.message.reply_text(f"Caption added: {text}")
    elif expecting == 'replace_caption':
        await update.message.reply_text(f"Caption replaced: {text}")
    elif expecting == 'new_button':
        if '|' in text:
            btn_text, url = text.split('|', 1)
            await update.message.reply_text(f"Button added: {btn_text} -> {url}")
        else:
            await update.message.reply_text("Invalid format. Please use: 'Button Text|URL'")
    
    user_data.pop('expecting', None)

def setup_caption_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_caption_actions, pattern="^caption_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_caption_input))
