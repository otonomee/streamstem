import yt_dlp
import random
import time
import logging
from fake_useragent import UserAgent


class Downloader:
    def __init__(self):
        self.ua = UserAgent()

    def get_ydl_opts(self, filetype):
        return {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": filetype,
                    "preferredquality": "192",
                }
            ],
            "outtmpl": "%(title)s.%(ext)s",
            "user_agent": self.ua.random,
            "http_headers": {
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.youtube.com/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": False,
            "no_warnings": False,
            "default_search": "auto",
            # "source_address": "0.0.0.0",
        }

    def download_video(self, youtube_url, filetype):
        ydl_opts = self.get_ydl_opts(filetype)
        max_retries = 3
        delay = 5

        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=True)
                    filename = ydl.prepare_filename(info)
                    return filename.rsplit(".", 1)[0] + "." + filetype
            except Exception as e:
                logging.error(f"Download attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(delay + random.uniform(1, 5))
                    ydl_opts["user_agent"] = (
                        self.ua.random
                    )  # Change user agent for each attempt
                else:
                    logging.error(f"Failed to download after {max_retries} attempts")
                    return None

    def get_video_info(self, youtube_url):
        ydl_opts = self.get_ydl_opts(
            "mp3"
        )  # Use mp3 as default, it doesn't matter for info extraction
        ydl_opts["extract_flat"] = True
        ydl_opts["skip_download"] = True

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(youtube_url, download=False)
        except Exception as e:
            logging.error(f"Failed to get video info: {str(e)}")
            return None
