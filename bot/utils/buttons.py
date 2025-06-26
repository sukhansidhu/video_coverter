from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
        keyboard_row = []
        for button_text in row:
            keyboard_row.append(InlineKeyboardButton(button_text, callback_data=button_text))
        keyboard.append(keyboard_row)
    
    return InlineKeyboardMarkup(keyboard)

def caption_editor_keyboard():
    buttons = [
        ["Add Caption", "Remove Caption"],
        ["Add Button", "Remove Button"],
        ["Add New Caption", "Forward Button"],
        ["Back", "Cancel"]
    ]
    
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button_text in row:
            keyboard_row.append(InlineKeyboardButton(button_text, callback_data=f"caption_{button_text.replace(' ', '_')}"))
        keyboard.append(keyboard_row)
    
    return InlineKeyboardMarkup(keyboard)

def metadata_editor_keyboard(streams):
    keyboard = []
    for stream in streams:
        stream_type = "Video" if stream['type'] == "video" else "Audio" if stream['type'] == "audio" else "Subtitle"
        title = stream['title'][:10] + "..." if len(stream['title']) > 10 else stream['title']
        btn_text = f"{stream_type} - {stream['codec']} - {stream['language']} {title}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"edit_stream_{stream['id']}")])
    
    keyboard.append([
        InlineKeyboardButton("All Audios", callback_data="edit_all_audios"),
        InlineKeyboardButton("All Subtitles", callback_data="edit_all_subs")
    ])
    keyboard.append([InlineKeyboardButton("Edit All Streams", callback_data="edit_all_streams")])
    keyboard.append([InlineKeyboardButton("Cancel Process", callback_data="cancel_process")])
    keyboard.append([InlineKeyboardButton("Upload Video", callback_data="upload_video")])
    
    return InlineKeyboardMarkup(keyboard)

def progress_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Progress", callback_data="show_progress")],
        [InlineKeyboardButton("Cancel", callback_data="cancel_download")]
    ])

def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="cancel_operation")]
    ])
