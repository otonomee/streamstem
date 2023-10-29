'''
This module handles the processing of audio using the demucs ml model.
'''
import subprocess
from tkinter import messagebox
class DemucsProcessor:
    def process_audio(self, audio_filename):
        '''
        Processes the audio file using the demucs ml model.
        '''
        try:
            subprocess.run(["python3", "-m", "demucs", "--mp3", audio_filename], check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to process audio.")