 # Web App for YouTube Audio Conversion using Demucs ML Model

## Introduction

This web application allows you to convert the audio from a YouTube video to separated stems using 
the Demucs ML model. It integrates the Demucs ML model and the youtube-dl package to provide a 
seamless audio conversion experience.

## Installation

To install and run the web app, please follow the steps below:

1. Install Python: Make sure you have Python installed on your machine. You can download Python 
from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Clone the repository: Open a terminal and clone the repository using the following command:

   ```
   git clone https://github.com/your-username/your-repo.git
   ```

3. Install dependencies: Navigate to the project directory and install the required dependencies 
by running the following command:

   ```
   pip install -r requirements.txt
   ```

4. Run the web app: Start the web app by running the following command:

   ```
   python main.py
   ```

5. Access the web app: Open your web browser and go to 
[http://localhost:5000](http://localhost:5000) to access the web app.

## Usage

1. Enter the YouTube video URL: On the web app's homepage, enter the URL of the YouTube video you 
want to convert the audio from.

2. Click the "Convert" button: After entering the YouTube video URL, click the "Convert" button to 
start the audio conversion process.

3. Wait for the conversion to complete: The web app will download the video and extract the audio 
using the youtube-dl package. Then, it will call the Demucs ML model to separate the audio into 
stems. Please wait for the conversion process to complete.

4. Download the separated stems: Once the conversion is finished, you will be able to download the 
separated stems. The stems will be saved in the same directory as the web app.

## Troubleshooting

If you encounter any issues while using the web app, please try the following troubleshooting 
steps:

1. Check the YouTube video URL: Make sure you have entered a valid YouTube video URL. The web app 
requires a valid URL to download the video and convert the audio.

2. Check your internet connection: Ensure that you have a stable internet connection to download 
the video and perform the audio conversion.

3. Verify the dependencies: Double-check that you have installed all the required dependencies 
mentioned in the installation steps. If any dependency is missing, please install it using the 
provided command.

4. Check the console output: If there are any error messages or exceptions displayed in the 
console, please review them to identify the cause of the issue.

If the issue persists, please reach out to our support team for further assistance.

## Conclusion

With this web app, you can easily convert the audio from YouTube videos to separated stems using 
the Demucs ML model. Enjoy exploring the different audio stems and unleash your creativity in 
music production and remixing!

If you have any feedback or suggestions for improving the web app, please feel free to contact us. 
We appreciate your input and strive to provide the best user experience possible.

Happy audio conversion!
