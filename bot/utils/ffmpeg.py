import os
import subprocess
import logging
from config import Config
from utils.helpers import get_media_info

logger = logging.getLogger(__name__)

def extract_thumbnail(video_path, output_dir):
    try:
        output_path = os.path.join(output_dir, "thumbnail.jpg")
        cmd = [
            Config.FFMPEG_PATH,
            "-i", video_path,
            "-ss", "00:00:01",
            "-vframes", "1",
            "-q:v", "2",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except Exception as e:
        logger.error(f"Thumbnail extraction failed: {str(e)}")
        return None

def edit_metadata(input_path, output_path, metadata):
    try:
        cmd = [Config.FFMPEG_PATH, "-i", input_path]
        
        for i, meta in enumerate(metadata):
            if meta.get('title') or meta.get('language'):
                cmd.extend(["-metadata", f"{meta['type']}:{i}={meta.get('title','')}"])
                if meta.get('language'):
                    cmd.extend(["-metadata", f"{meta['type']}:{i}:language={meta['language']}"])
        
        cmd.extend(["-c", "copy", output_path])
        
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except Exception as e:
        logger.error(f"Metadata editing failed: {str(e)}")
        return None

def merge_videos(video_paths, output_path):
    try:
        list_path = os.path.join(Config.UPLOAD_PATH, "filelist.txt")
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{os.path.basename(path)}'\n")
        
        cmd = [
            Config.FFMPEG_PATH,
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path
    except Exception as e:
        logger.error(f"Video merging failed: {str(e)}")
        return None

def trim_video(input_path, output_path, start_time, end_time):
    try:
        cmd = [
            Config.FFMPEG_PATH,
            "-i", input_path,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path
    except Exception as e:
        logger.error(f"Video trimming failed: {str(e)}")
        return None

def convert_video(input_path, output_path, format):
    try:
        cmd = [
            Config.FFMPEG_PATH,
            "-i", input_path,
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path
    except Exception as e:
        logger.error(f"Video conversion failed: {str(e)}")
        return None
