from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
import os
import sys

sys.path.append(os.path.abspath("demucs"))
import glob
import shutil
from downloader import Downloader
from demucs_processor import DemucsProcessor
from spotify_to_yt import ConvertSpofity
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.datastructures import URL
from starlette.responses import RedirectResponse

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)
downloader = Downloader()


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

global filename
demucs_processor = DemucsProcessor(num_threads=4, segment_size=7)
downloader = Downloader()


class DownloadRequest(BaseModel):
    url: str
    filetype: str


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
    file_path = f"tracks/{stem_type}/{songname}/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


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
