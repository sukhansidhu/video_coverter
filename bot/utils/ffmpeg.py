import os
import subprocess
import logging
from bot.config import Config  # ✅ Make sure it's imported with correct path

logger = logging.getLogger(__name__)

def extract_thumbnail(video_path, output_dir):
    """Extract a single thumbnail frame from the video."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "thumbnail.jpg")
        cmd = [
            Config.FFMPEG_PATH,
            "-i", video_path,
            "-ss", "00:00:01",
            "-vframes", "1",
            "-q:v", "2",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"❌ Thumbnail extraction failed: {e}")
        return None

def edit_metadata(input_path, output_path, metadata):
    """
    Edit stream metadata (title/language) using FFmpeg.
    'metadata' should be a list of dicts with keys: 'type' ('audio'/'subtitle'), 'title', and 'language'.
    Example:
        [{"type": "audio", "title": "English Audio", "language": "eng"}]
    """
    try:
        cmd = [Config.FFMPEG_PATH, "-i", input_path, "-map", "0"]
        for i, meta in enumerate(metadata):
            stream_flag = meta['type'][0]  # 'a' for audio, 's' for subtitle
            if meta.get('title'):
                cmd.extend(["-metadata:s:{}:{}".format(stream_flag, i), f"title={meta['title']}"])
            if meta.get('language'):
                cmd.extend(["-metadata:s:{}:{}".format(stream_flag, i), f"language={meta['language']}"])
        cmd.extend(["-c", "copy", output_path])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"❌ Metadata editing failed: {e}")
        return None

def merge_videos(video_paths, output_path):
    """Merge multiple videos using FFmpeg concat demuxer."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        list_path = os.path.join(Config.UPLOAD_PATH, "filelist.txt")
        with open(list_path, "w", encoding='utf-8') as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        cmd = [
            Config.FFMPEG_PATH,
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"❌ Video merging failed: {e}")
        return None

def trim_video(input_path, output_path, start_time, end_time):
    """Trim a video using start and end time."""
    try:
        cmd = [
            Config.FFMPEG_PATH,
            "-i", input_path,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"❌ Video trimming failed: {e}")
        return None

def convert_video(input_path, output_path):
    """Convert video to a different format based on the output file extension."""
    try:
        cmd = [
            Config.FFMPEG_PATH,
            "-i", input_path,
            "-preset", "fast",  # Optional: speeds up processing, higher CPU
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"❌ Video conversion failed: {e}")
        return None
