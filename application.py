from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import sys
import glob
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.abspath("demucs"))

from downloader import Downloader
from demucs_processor import DemucsProcessor
from spotify_to_yt import ConvertSpofity
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import URL
from starlette.responses import RedirectResponse

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)


class DownloadRequest(BaseModel):
    url: str
    filetype: str


#@app.middleware("https")
#async def https_redirect(request, call_next):
#    if request.url.scheme == "http":
#        url = request.url.replace(scheme="https")
#        return RedirectResponse(url, status_code=301)
#    return await call_next(request)


# Add CORS middleware if needed


#class CSPMiddleware(BaseHTTPMiddleware):
#    async def dispatch(self, request, call_next):
#        response = await call_next(request)
#        response.headers["Content-Security-Policy"] = "upgrade-insecure-requests"
#        return response


#app.add_middleware(CSPMiddleware)

# app.add_middleware(CSPMiddleware)
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["https://streamstem-60192b39b74f.herokuapp.com"],
# )

#app.add_middleware(
#    CORSMiddleware,
    # allow_origins=["https://streamstem-60192b39b74f.herokuapp.com"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)
# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mount the static directory
app.mount(
    "/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static"
)

# Set up Jinja2 templates
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# Initialize processors
demucs_processor = DemucsProcessor(num_threads=4, segment_size=7)
downloader = Downloader()


class ProcessRequest(BaseModel):
    filename: str
    filetype: str
    numStems: int


@app.get("/")
async def home(request: Request):
    refresh_directories()
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/delete")
async def delete(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download_video")
async def download_audio(request: DownloadRequest):
    filename = downloader.download_video(request.url, request.filetype)
    if filename:
        return {"status": "success", "filename": filename}
    else:
        raise HTTPException(status_code=400, detail="Failed to download video")


@app.get("/video_info")
async def get_video_info(url: str):
    info = downloader.get_video_info(url)
    if info:
        return {"status": "success", "info": info}
    else:
        raise HTTPException(status_code=400, detail="Failed to get video info")


@app.post("/process_audio")
async def process_audio(request: ProcessRequest):
    demucs_processor.process_audio(request.filename, request.filetype, request.numStems)
    return {"message": "Finished", "filename": str(request.filename)}


@app.get("/download")
async def download(filename: str):
    file_path = f"{filename}.zip"
    if os.path.exists(file_path):
        response = FileResponse(file_path, filename=os.path.basename(file_path))
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/tracks/{stem_type}/{songname}")
async def serve_audio(stem_type: str, songname: str):
    directory = f"tracks/{stem_type}/{songname}"
    if os.path.exists(directory):
        files = os.listdir(directory)
        return JSONResponse(content=files)
    else:
        raise HTTPException(status_code=404, detail="Directory not found")


@app.get("/tracks/{stem_type}/{songname}/{filename}")
async def serve_file(stem_type: str, songname: str, filename: str):
    """
    Serve audio stem files with path traversal protection.

    Args:
        stem_type: Model type (htdemucs or htdemucs_6s)
        songname: Name of the song
        filename: Name of the file

    Raises:
        HTTPException: If path is invalid or file not found
    """
    # Validate stem_type to prevent directory traversal
    allowed_stem_types = ["htdemucs", "htdemucs_6s"]
    if stem_type not in allowed_stem_types:
        raise HTTPException(status_code=400, detail="Invalid stem type")

    # Sanitize path components to prevent directory traversal
    # Remove any path separators, null bytes, and parent directory references
    safe_stem_type = stem_type.replace("..", "").replace("/", "").replace("\\", "").replace("\0", "")
    safe_songname = songname.replace("..", "").replace("/", "").replace("\\", "").replace("\0", "")
    safe_filename = filename.replace("..", "").replace("/", "").replace("\\", "").replace("\0", "")

    # Construct path
    file_path = os.path.join("tracks", safe_stem_type, safe_songname, safe_filename)

    # Resolve to absolute path and verify it's within tracks directory
    tracks_dir = os.path.abspath("tracks")
    absolute_path = os.path.abspath(file_path)

    # Ensure the resolved path is within tracks directory (prevent path traversal)
    if not absolute_path.startswith(tracks_dir):
        raise HTTPException(status_code=403, detail="Access denied")

    # Check if file exists
    if not os.path.exists(absolute_path) or not os.path.isfile(absolute_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(absolute_path)


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


def refresh_directories():
    for directory in glob.glob("tracks/htdemucs/*"):
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    for directory in glob.glob("tracks/htdemucs_6s/*"):
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    for file in glob.glob("*.mp3") + glob.glob("*.wav") + glob.glob("*.flac"):
        os.remove(file)


@app.get("/flaskwebgui-keep-server-alive")
async def keep_alive():
    return {"status": "Server is alive"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8001)))
