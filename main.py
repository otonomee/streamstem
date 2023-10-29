'''
This is the main module of the web app that integrates the demucs ml model and the youtube-dl package.
'''
import tkinter as tk
from tkinter import messagebox
from downloader import Downloader
from demucs_processor import DemucsProcessor
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Audio Converter")
        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_audio)
        self.convert_button.pack()
        self.downloader = Downloader()
        self.demucs_processor = DemucsProcessor()
    def convert_audio(self):
        youtube_url = self.url_entry.get()
        if not youtube_url:
            messagebox.showerror("Error", "URL is required.")
            return
        video_filename = self.downloader.download_video(youtube_url)
        if not video_filename:
            messagebox.showerror("Error", "Failed to download video.")
            return
        audio_filename = self.downloader.get_output_filename(video_filename)
        if not audio_filename:
            messagebox.showerror("Error", "Failed to get output filename.")
            return
        self.demucs_processor.process_audio(audio_filename)
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    app = App()
    app.run()