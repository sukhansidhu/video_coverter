from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Main menu layout
def main_menu_keyboard():
    buttons = [
        ["Thumbnail Extractor", "Caption And Buttons Editor", "Metadata Editor"],
        ["Media Forwarder", "Stream Remover", "Stream Extractor"],
        ["Video Trimmer", "Video Merger", "Remove Audio"],
        ["Merge 💷️ And 💷️", "Audio Converter", "Videos Splitter"],
        ["Screenshots", "Manual Shots", "Generate Sample"],
        ["Video To Audio", "Video Optimizer", "Subtitle Merger"],
        ["Video Converter", "Video Renamer", "Media Information"],
        ["Create Archive", "Cancel X"]
    ]
    
    keyboard = []
    for row in buttons:
        keyboard_row = [
            InlineKeyboardButton(text, callback_data=text) for text in row
        ]
        keyboard.append(keyboard_row)
    
    return InlineKeyboardMarkup(keyboard)

# Caption/Buttons editor menu
def caption_editor_keyboard():
    buttons = [
        ["Add Caption", "Remove Caption"],
        ["Add Button", "Remove Button"],
        ["Add New Caption", "Forward Button"],
        ["Back", "Cancel"]
    ]
    
    keyboard = []
    for row in buttons:
        keyboard_row = [
            InlineKeyboardButton(text, callback_data=f"caption_{text.replace(' ', '_')}") for text in row
        ]
        keyboard.append(keyboard_row)
    
    return InlineKeyboardMarkup(keyboard)

# Metadata stream selection
def metadata_editor_keyboard(streams):
    keyboard = []
    for stream in streams:
        stream_type = stream['type'].capitalize()
        codec = stream['codec']
        lang = stream['language']
        title = stream['title'][:10] + "..." if len(stream['title']) > 10 else stream['title']
        
        btn_text = f"{stream_type} - {codec} - {lang} {title}"
        callback = f"edit_stream_{stream['id']}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback)])
    
    keyboard.append([
        InlineKeyboardButton("All Audios", callback_data="edit_all_audios"),
        InlineKeyboardButton("All Subtitles", callback_data="edit_all_subs")
    ])
    keyboard.append([
        InlineKeyboardButton("Edit All Streams", callback_data="edit_all_streams")
    ])
    keyboard.append([
        InlineKeyboardButton("Cancel Process", callback_data="cancel_process")
    ])
    keyboard.append([
        InlineKeyboardButton("Upload Video", callback_data="upload_video")
    ])
    
    return InlineKeyboardMarkup(keyboard)

# Show progress/cancel
def progress_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Progress", callback_data="show_progress")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]
    ])

# Generic cancel
def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_operation")]
    ])
