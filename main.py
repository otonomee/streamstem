from flask import Response, jsonify, Flask, send_file, request, render_template, redirect, url_for, send_from_directory
from downloader import Downloader
from demucs_processor import DemucsProcessor
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread

app = Flask(__name__)
# downloader = Downloader()
demucs_processor = DemucsProcessor()

@app.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     youtube_url = request.form.get('url')
    #     if youtube_url:
    #         print(youtube_url)
    #         demucs_processor.process_audio('test.mp3')
        
    return render_template('index.html')

from queue import Queue
from threading import Thread

@app.route('/process_audio', methods=['POST', 'GET'])
def process_audio():
    def process_audio_and_report_progress(queue):
        for i in range(30):
            # Replace this with actual processing code
            time.sleep(1)
            queue.put(f"Progress: {i+1}/30")

    def generate():
        queue = Queue()
        thread = Thread(target=process_audio_and_report_progress, args=(queue,))
        thread.start()

        while True:
            if not queue.empty():
                progress = queue.get()
                yield f"data: {progress}\n\n"
            else:
                yield f"data: Processing...\n\n"
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')
# @app.route('/process_audio', methods=['POST'])
# def process_audio():    
#     global process
#     audio_filename = request.json.get('audio_filename')
#     print(audio_filename)
#     demucs_processor.process_audio(audio_filename)
#     return jsonify({'message': 'Processing started'}), 202

@app.route('/download', methods=['GET'])
def download():
    return send_file('separated.zip', as_attachment=True)

# @app.route('/check_process')
# def check_process():
#     if process is None:
#         return jsonify({'status': 'no process'})
#     elif process.poll() is None:
#         return jsonify({'status': 'running'})
#     else:
#         return jsonify({'status': 'finished', 'exit_code': process.poll()})
    
# @app.route('/download/<path:filename>')
# def download(filename):
#     return send_from_directory(directory='separated/htdemucs/', filename=filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)