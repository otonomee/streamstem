#!/bin/bash

get_youtube_url() {
    read -p "Enter artist name: " artist_names
    read -p "Enter track name: " track_name

    # URL encode the artist name and track name
    artist_names_encoded=$(jq -nr --arg v "$artist_names" '$v|@uri')
    track_name_encoded=$(jq -nr --arg v "$track_name" '$v|@uri')

    # Read the Google API key from config.json
    google_api_key=$(jq -r '.google_api_key' config.json)
    # echo "Google API Key: $google_api_key"  # Debug print

    url="https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=${artist_names_encoded}%20${track_name_encoded}&type=video&key=${google_api_key}"
    # echo "URL: $url"  # Debug print

    response=$(curl -s "$url")
    video_id=$(echo "$response" | jq -r '.items[0].id.videoId')
    # echo "Video ID: $video_id"  # Debug print

    echo "https://www.youtube.com/watch?v=${video_id}"
}

echo "1. Enter YouTube URL directly"
echo "2. Enter search query"
read -p "Enter your choice (1 or 2): " choice
echo "Choice: $choice"  # Debug print

if [ "$choice" -eq 1 ]; then
    read -p "Enter the YouTube video URL: " youtube_url
elif [ "$choice" -eq 2 ]; then
    youtube_url=$(get_youtube_url)
else
    echo "Invalid choice."
    exit 1
fi

echo "YouTube URL: $youtube_url"  # Debug print

if [ -z "$youtube_url" ]; then
    echo "URL is required."
    exit 1
fi

output_filename=$(youtube-dl --get-filename -o "%(title)s.mp3" "$youtube_url")
echo "Output filename: $output_filename"  # Debug print

# Download the video and extract audio with youtube-dl
youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.mp3" $youtube_url

# Call your Python script with the downloaded MP3 file
python3 -m demucs --mp3 "$output_filename"