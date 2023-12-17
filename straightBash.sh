#!/bin/bash

echo "Enter the YouTube video URL:"
read youtube_url

if [ -z "$youtube_url" ]; then
    echo "URL is required."
    exit 1
fi

output_filename=$(youtube-dl --get-filename -o "%(title)s.mp3" "$youtube_url")

# Download the video and extract audio with youtube-dl
youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.mp3" $youtube_url

# Call your Python script with the downloaded MP3 file
python3 -m demucs --mp3 "$output_filename"

