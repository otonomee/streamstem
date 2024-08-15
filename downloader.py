import subprocess
from fake_useragent import UserAgent

zyte_proxy_key = "f870f1fc51dc43848e44c2795ea1a154"
zyte_api_key = "da91cf171873419d90bf6ae752409a57"


class Downloader:
    def __init__(self):

        self.ua = UserAgent()
        self.zyte_proxy = f"http://{zyte_proxy_key}:@proxy.crawlera.com:8011/"

    def download_video(self, youtube_url, filetype):
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "--extract-audio",
                    "--audio-format",
                    filetype,
                    "-o",
                    "%(title)s.%(ext)s",
                    "--proxy",
                    self.zyte_proxy,
                    # "--user-agent",
                    # self.ua.random,
                    youtube_url,
                ],
                check=True,
            )
            output_filename = self.get_output_filename(youtube_url)
            return str(output_filename)
        except subprocess.CalledProcessError as e:
            print(f"Error downloading video: {e}")
            return None

    def get_output_filename(self, youtube_url):
        try:
            output = subprocess.check_output(
                [
                    "yt-dlp",
                    "--get-filename",
                    "-o",
                    "%(title)s.%(ext)s",
                    "--proxy",
                    self.zyte_proxy,
                    # "--user-agent",
                    # self.ua.random,
                    youtube_url,
                ]
            )
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting filename: {e}")
            return None

    def get_video_info(self, youtube_url):
        try:
            output = subprocess.check_output(
                [
                    "yt-dlp",
                    "--dump-json",
                    "--proxy",
                    self.zyte_proxy,
                    # "--user-agent",
                    # self.ua.random,
                    youtube_url,
                ]
            )
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting video info: {e}")
            return None


# Usage example:
# downloader = Downloader(zyte_api_key="your_zyte_api_key_here")
# filename = downloader.download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "mp3")
# video_info = downloader.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
