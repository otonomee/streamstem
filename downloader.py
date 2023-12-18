import subprocess

class Downloader:
    def download_video(self, youtube_url, filetype):
        try:
            subprocess.run(["yt-dlp", "--extract-audio", "--audio-format", filetype, "-o", "%(title)s", youtube_url, "--force-ipv6"], check=True)
            output_filename = self.get_output_filename(youtube_url)
            return str(output_filename)
        except subprocess.CalledProcessError:
            return None

    def get_output_filename(self, youtube_url):
        try:
            output = subprocess.check_output(["yt-dlp", "--get-filename", "-o", "%(title)s", youtube_url])
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            return None
