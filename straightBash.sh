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

# Prefer yt-dlp; bail if missing
YT_DLP_BIN="${YT_DLP_BIN:-yt-dlp}"
if ! command -v "$YT_DLP_BIN" >/dev/null 2>&1; then
    echo "Error: yt-dlp is required but not found in PATH (tried '$YT_DLP_BIN')."
    echo "Install with: pipx install yt-dlp   or   brew install yt-dlp"
    exit 1
fi

# Use explicit python path if provided, else default python3
PYTHON_PATH="${PYTHON_PATH:-/opt/homebrew/Caskroom/miniconda/base/bin/python}"

# Ensure demucs is available in this Python interpreter
if ! "$PYTHON_PATH" - <<'PY' >/dev/null 2>&1
import importlib.util
exit(0 if importlib.util.find_spec("demucs") else 1)
PY
then
    echo "Error: demucs is not installed for $("$PYTHON_PATH" -V)."
    echo "Install with: $PYTHON_PATH -m pip install -U demucs"
    exit 1
fi

# Get filename (force mp3 extension to match extract-audio output)
output_filename=$("$YT_DLP_BIN" --get-filename -o "%(title)s.mp3" "$youtube_url")
echo "Output filename: $output_filename"  # Debug print

# Download the video and extract audio
"$YT_DLP_BIN" --extract-audio --audio-format mp3 -o "%(title)s.mp3" "$youtube_url"

# Separate stems with demucs
"$PYTHON_PATH" -m demucs --mp3 "$output_filename"

# Rename stems to include directory name (matches youtube-to-audio-stems.sh behavior)
stem_dir="separated/htdemucs/${output_filename%.mp3}"
if [ -d "$stem_dir" ]; then
    dir_name=$(basename "$stem_dir")
    for stem in "$stem_dir"/*.mp3; do
        stem_name=$(basename "$stem")
        mv "$stem" "$stem_dir/$dir_name - $stem_name"
    done
    echo "Stems renamed in: $stem_dir"
fi