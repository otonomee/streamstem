'''
This module handles the downloading of videos using youtube-dl.
'''
import subprocess
class Downloader:
    def download_video(self, youtube_url):
        '''
        Downloads the video from the given YouTube URL and returns the downloaded video filename.
        '''
        try:
            subprocess.run(["yt-dlp", "--extract-audio", "--audio-format", "mp3", "-o", "%(title)s", youtube_url], check=True)
            output_filename = self.get_output_filename(youtube_url)
            return str(output_filename) + ".mp3"
        except subprocess.CalledProcessError:
            return None
    def get_output_filename(self, youtube_url):
        '''
        Retrieves the output filename of the downloaded video.
        '''
        try:
            output = subprocess.check_output(["yt-dlp", "--get-filename", "-o", "%(title)s", youtube_url])
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            return None