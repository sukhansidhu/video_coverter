from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# 🧭 Main menu layout
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
    
    keyboard = [
        [InlineKeyboardButton(text, callback_data=text)] for row in buttons for text in row
    ]
    
    return InlineKeyboardMarkup(keyboard)

# 📝 Caption and Button Editor
def caption_editor_keyboard():
    buttons = [
        ["Add Caption", "Remove Caption"],
        ["Add Button", "Remove Button"],
        ["Add New Caption", "Forward Button"],
        ["Back", "Cancel"]
    ]

    keyboard = [
        [
            InlineKeyboardButton(text, callback_data=f"caption_{text.replace(' ', '_')}")
            for text in row
        ]
        for row in buttons
    ]

    return InlineKeyboardMarkup(keyboard)

# 🧾 Metadata stream selection (used after analyzing video)
def metadata_editor_keyboard(streams):
    keyboard = []
    for stream in streams:
        stream_type = stream.get('type', 'Unknown').capitalize()
        codec = stream.get('codec', 'N/A')
        lang = stream.get('language', 'N/A')
        title = stream.get('title', 'None')
        short_title = (title[:10] + "...") if len(title) > 10 else title

        btn_text = f"{stream_type} - {codec} - {lang} {short_title}"
        callback = f"edit_stream_{stream['id']}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback)])

    keyboard.extend([
        [InlineKeyboardButton("Edit All Streams", callback_data="edit_all_streams")],
        [InlineKeyboardButton("Upload Video", callback_data="upload_video")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]
    ])
    
    return InlineKeyboardMarkup(keyboard)

# 📊 Show download progress + cancel option
def progress_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Progress", callback_data="show_progress")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]
    ])

# ❌ Generic cancel for any operation
def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]
    ])
