from flask import Flask, request, render_template, redirect, url_for
from downloader import Downloader
from demucs_processor import DemucsProcessor

app = Flask(__name__)
downloader = Downloader()
demucs_processor = DemucsProcessor()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        youtube_url = request.form.get('url')
        print(youtube_url)
        if not youtube_url:
            return render_template('index.html', error="URL is required.")
        video_filename = downloader.download_video(youtube_url)
        if not video_filename:
            return render_template('index.html', error="Failed to download video.")
        audio_filename = downloader.get_output_filename(video_filename)
        if not audio_filename:
            return render_template('index.html', error="Failed to get output filename.")
        demucs_processor.process_audio(audio_filename)
        return redirect(url_for('download', filename=audio_filename))
    return render_template('index.html')

# @app.route('/download/<filename>')
# def download(filename):
#     # Implement your file download logic here
#     pass

if __name__ == "__main__":
    app.run(debug=True)