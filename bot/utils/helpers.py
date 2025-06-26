import os
import re
import math
import time
from datetime import datetime
from pymediainfo import MediaInfo

def get_file_size(size_in_bytes):
    if size_in_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    return f"{s} {size_name[i]}"

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '', filename)

def generate_unique_filename(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while True:
        new_filename = f"{base}_{counter}{ext}" if counter > 1 else filename
        if not os.path.exists(os.path.join(directory, new_filename)):
            return new_filename
        counter += 1

def get_media_info(file_path):
    media_info = MediaInfo.parse(file_path)
    info = {}
    
    for track in media_info.tracks:
        if track.track_type == "Video":
            info["video"] = {
                "codec": track.codec_id or track.format,
                "duration": track.duration,
                "resolution": f"{track.width}x{track.height}",
                "bitrate": track.bit_rate,
                "frame_rate": track.frame_rate
            }
        elif track.track_type == "Audio":
            info.setdefault("audio", []).append({
                "codec": track.codec_id or track.format,
                "language": track.language or "None",
                "title": track.title or "None",
                "channels": track.channel_s,
                "bitrate": track.bit_rate
            })
        elif track.track_type == "Text":
            info.setdefault("subtitle", []).append({
                "codec": track.codec_id or track.format,
                "language": track.language or "None",
                "title": track.title or "None"
            })
    
    return info
