from flask import Response, jsonify, Flask, send_file, request, render_template
from downloader import Downloader
from demucs_processor import DemucsProcessor
import os
import glob

app = Flask(__name__)
global filename

# downloader = Downloader()
demucs_processor = DemucsProcessor()
downloader = Downloader()

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/download_video', methods=['POST'])
def download_audio():
    if request.method == 'POST':
        youtube_url = request.json.get('url')
        filetype = request.json.get('filetype')
        if youtube_url:
            filename = downloader.download_video(youtube_url, filetype)
            print('filename', filename)
    return jsonify({'status': 'success', 'filename': str(filename)})

def progress_check(d):
    if d['status'] == 'finished':
        print('RUN DEMUCS')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    filename = request.json.get('filename')
    filetype = request.json.get('filetype')
    num_stems = request.json.get('numStems')
    demucs_processor.process_audio(filename, filetype, num_stems)
    # requests.get('http://localhost:5000/download')
    return jsonify({'message': 'Finished', 'filename': str(filename)})

@app.route('/download', methods=['POST', 'GET'])
def download():
    filename = request.args.get('filename')
    response = send_file(f"{filename}.zip", as_attachment=True)

    # Delete the .zip file after sending it
    if os.path.exists(f"{filename}.zip"):
        os.remove(f"{filename}.zip")

    # Delete any .mp3 or .wav files
    for file in glob.glob("*.mp3"):
        os.remove(file)
    for file in glob.glob("*.wav"):
        os.remove(file)

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
