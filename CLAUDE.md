# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StreamStem is a FastAPI web application that extracts audio stems (vocals, drums, bass, etc.) from YouTube or Spotify URLs using the Demucs machine learning model. The app downloads audio via yt-dlp, processes it through Demucs for source separation, and returns downloadable stems in various formats.

## Architecture

### Core Components

**FastAPI Application (application.py)**
- Main web server using FastAPI framework
- Handles HTTP endpoints for download, processing, and file serving
- Orchestrates the download → process → serve workflow
- Uses Jinja2 templates for frontend rendering
- Runs on uvicorn/gunicorn in production

**Downloader (downloader.py)**
- Wraps yt-dlp to extract audio from YouTube videos
- Downloads audio in user-specified format (mp3, wav, flac)
- Returns sanitized filename for subsequent processing

**Demucs Processor (demucs_processor.py)**
- Executes Demucs ML model as a subprocess
- Supports 2-stem (vocals/instrumental), 4-stem (vocals/drums/bass/other), or 6-stem separation
- Uses htdemucs or htdemucs_6s models depending on stem count
- Configurable threading and segment size for performance tuning
- Creates zip archives of separated stems

**Spotify Converter (spotify_to_yt.py)**
- Converts Spotify track URLs to YouTube URLs
- Uses Spotify API to fetch track/artist metadata
- Queries YouTube Data API to find matching video
- API credentials stored in config.json

### Request Flow

1. User submits YouTube/Spotify URL via web interface
2. Frontend calls `/download_video` endpoint with URL and desired format
3. Downloader fetches audio using yt-dlp
4. Frontend calls `/process_audio` with filename, format, and stem count
5. DemucsProcessor runs separation model on downloaded audio
6. Separated stems are zipped and made available at `/download`
7. Individual stems can be streamed via `/tracks/{stem_type}/{songname}/{filename}`

### Frontend

- Vanilla JavaScript (static/js/main.js) handles form submission and API calls
- TailwindCSS for styling (configured via tailwind.config.js)
- Custom CSS in static/css/style.css
- Jinja2 templates in templates/

## Development Commands

### Running the Application

**Local development:**
```bash
python application.py
```
The app runs on http://0.0.0.0:8001 by default (port configurable via PORT env var).

**Docker:**
```bash
docker build -t streamstem .
docker run -p 8000:8000 streamstem
```

### CSS Development

**Build Tailwind CSS:**
```bash
npm run build:css
```

**Watch mode for development:**
```bash
npm run dev:css
```

Input: `static/css/tailwind-input.css` → Output: `static/css/tailwind.css`

## Key Configuration

**DemucsProcessor Parameters (application.py:81)**
- `num_threads=4`: Number of CPU threads for processing
- `segment_size=7`: Audio segment length in seconds (lower = faster but less accurate)

**Demucs Command Construction (demucs_processor.py:50-71)**
- Model selection based on stem count
- CPU-only mode (`-d cpu`) - no GPU support currently
- Overlap set to 0.1 for speed optimization
- Two-stems mode filters to vocals/instrumental only

**API Credentials (config.json)**
- Contains Spotify client ID/secret and Google API key
- Required for Spotify URL conversion feature
- **Warning**: This file contains sensitive credentials and should not be committed

## Important Notes

### File Cleanup
The `refresh_directories()` function (application.py:170-178) runs on every home page load and deletes:
- All content in `tracks/htdemucs/`
- All content in `tracks/htdemucs_6s/`
- All .mp3, .wav, .flac files in root directory

This aggressive cleanup prevents disk space issues but means no persistence between sessions.

### Demucs Submodule
The `demucs/` directory is a git submodule of the Facebook Research Demucs project. The app executes Demucs via subprocess calls to `python -m demucs.separate` rather than importing it as a library.

### URL Validation
Frontend validates YouTube and Spotify URLs with regex patterns (main.js:33-36):
- YouTube: `youtube.com/watch?v=` and `youtu.be/` formats
- Spotify: `open.spotify.com/track/` format (requires 22-char track ID)

### Output Structure
Separated stems are stored in:
```
tracks/
  htdemucs/          # 2 or 4 stem outputs
    {songname}/
      vocals.{ext}
      drums.{ext}
      bass.{ext}
      other.{ext}
  htdemucs_6s/       # 6 stem outputs
    {songname}/
      vocals.{ext}
      drums.{ext}
      bass.{ext}
      guitar.{ext}
      piano.{ext}
      other.{ext}
```

Zip archives are created in root as `STEMS-{songname}.zip`.
