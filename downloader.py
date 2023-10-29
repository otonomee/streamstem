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
            subprocess.run(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "-o", "%(title)s.mp3", youtube_url], check=True)
            output_filename = self.get_output_filename(youtube_url)
            return output_filename
        except subprocess.CalledProcessError:
            return None
    def get_output_filename(self, video_filename):
        '''
        Retrieves the output filename of the downloaded video.
        '''
        try:
            output = subprocess.check_output(["youtube-dl", "--get-filename", "-o", "%(title)s.mp3", video_filename])
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            return None